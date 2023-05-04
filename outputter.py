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


def pretty_print_per_participant(participants, assignments, topic_indexes, csv=True):
    for participant in participants:
        topics = [topic_indexes[i] for i in _get_topics_in_order(participant, assignments)]
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

    html_body = f'''
    <html><body><p>Dear {participant.name},</p>
    
    <p>
    We would like to inform you that you have been assigned the following topics for each of the brainstorming rounds in the FRDN event:
    <ul>
        <li>For the first round, 'Dream', your assigned topic is '<b>{_TOPIC_NAMES[topics[0]]}</b>'.</li>
        <li>For the second round, 'Design', your assigned topic is '<b>{_TOPIC_NAMES[topics[1]]}</b>'.</li>
        <li>For the last round, 'Deliver', your assigned topic is '<b>{_TOPIC_NAMES[topics[2]]}</b>'.</li>
    </ul>
    To find the location of your assigned topics table, please refer to the venue map that you have received.    </p>
    
    <p>Thank you, and best regards,<br>
    The FRDN team</p></body></html>'''
    html_body_with_rtf = "{\\rtf1\\ansi\\ansicpg1252\\fromhtml1 \\htmlrtf0 " + html_body + "}"
    rtf_body = html_body_with_rtf.encode("utf_8")

    message.body_html_text = html_body
    message.body_rtf = rtf_body

    message.display_to = participant.email
    # message.display_cc = "Mary Smith"
    message.recipients.append(recipient)
    message.message_flags.append(MessageFlag.UNSENT)
    message.store_support_masks.append(StoreSupportMask.CREATE)

    message.save(f'emails/email_{participant.name}_{participant.id}.msg')
