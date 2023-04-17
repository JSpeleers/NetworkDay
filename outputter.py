from independentsoft.msg import DisplayType
from independentsoft.msg import Message
from independentsoft.msg import MessageFlag
from independentsoft.msg import ObjectType
from independentsoft.msg import Recipient
from independentsoft.msg import RecipientType
from independentsoft.msg import StoreSupportMask


def pretty_print(assignments):
    for i, r in enumerate(assignments):
        print(f'Round {i + 1}')
        for t, topic in enumerate(r):
            print(f'\tTopic {t + 1}:\t{topic}')


def pretty_print_per_participant(participants, assignments, csv=True):
    for participant in participants:
        topics = [t for i, r in enumerate(assignments) for t, topic in enumerate(r) if participant in topic]
        if csv:
            print(f'{participant},{",".join(map(str, topics))}')
        else:
            print(f'{participant}: {topics}')


def solution_to_emails(participants, assignments):
    for participant in participants:
        topics = [t for i, r in enumerate(assignments) for t, topic in enumerate(r) if participant in topic]
        _create_msg(participant, topics)


def _create_msg(participant, topics, subject='Email title'):
    message = Message()

    recipient = Recipient()
    recipient.address_type = "SMTP"
    recipient.display_type = DisplayType.MAIL_USER
    recipient.object_type = ObjectType.MAIL_USER
    recipient.display_name = participant.name
    recipient.email_address = participant.email
    recipient.recipient_type = RecipientType.TO

    message.subject = subject
    message.body = f'''Beste {participant.name},
    
    U volgt de volgende onderwerpen: {",".join(map(str, topics))}
    
    Veel plezier!
    '''
    message.display_to = "John Smith"
    message.display_cc = "Mary Smith"
    message.recipients.append(recipient)
    message.message_flags.append(MessageFlag.UNSENT)
    message.store_support_masks.append(StoreSupportMask.CREATE)

    message.save(f'emails/email_{participant.name}_{participant.id}.msg')
