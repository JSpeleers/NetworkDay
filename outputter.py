from independentsoft.msg import DisplayType
from independentsoft.msg import Message
from independentsoft.msg import MessageFlag
from independentsoft.msg import ObjectType
from independentsoft.msg import Recipient
from independentsoft.msg import RecipientType
from independentsoft.msg import StoreSupportMask

_TOPIC_NAMES = ['Human resources', 'Rewards and incentives', 'Legal aspects', 'Infrastructure', 'Reuse of data',
                'Quality of research', 'Open Access for publications', 'Societal role', 'Digital innovation',
                'Change of mindset']


def pretty_print(assignments):
    for i, r in enumerate(assignments):
        print(f'Round {i + 1}')
        for t, topic in enumerate(r):
            print(f'\tTopic {t + 1}:\t{topic}')


def pretty_print_per_participant(participants, assignments, csv=True):
    for participant in participants:
        topics = _get_topics_in_order(participant, assignments)
        if csv:
            print(f'{participant},{",".join(map(str, topics))}')
        else:
            print(f'{participant}: {topics}')


def solution_to_emails(participants, assignments):
    for participant in participants:
        print(f'Creating email for {participant}')
        _create_msg(participant, _get_topics_in_order(participant, assignments))


def _get_topics_in_order(participant, assignments):
    return [t for _, r in enumerate(assignments) for t, topic in enumerate(r) if participant in topic]


def _create_msg(participant, topics, subject='Topics Brainstormsessions Open Science NetworkDay'):
    message = Message()

    recipient = Recipient()
    recipient.address_type = "SMTP"
    recipient.display_type = DisplayType.MAIL_USER
    recipient.object_type = ObjectType.MAIL_USER
    recipient.display_name = participant.email
    recipient.email_address = participant.email
    recipient.recipient_type = RecipientType.TO

    message.subject = subject
    message.body = f'''Dear {participant.name},

For brainstorm round 1 'Dream', you have been assigned to topic '{_TOPIC_NAMES[topics[0]]}'. For the second round 'Design' you have been assigned to topic '{_TOPIC_NAMES[topics[1]]}'. For the last round 'Deliver' you have been assigned to topic '{_TOPIC_NAMES[topics[2]]}'.
You can find your topic table on the map you received.

Best regards,
The FRDN team
    '''

    message.display_to = participant.email
    # message.display_cc = "Mary Smith"
    message.recipients.append(recipient)
    message.message_flags.append(MessageFlag.UNSENT)
    message.store_support_masks.append(StoreSupportMask.CREATE)

    message.save(f'emails/email_{participant.name}_{participant.id}.msg')
