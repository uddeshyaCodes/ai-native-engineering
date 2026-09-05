type Email = {type: 'email', emailId: string};
type SMS = {type: 'sms', phoneNumber: string};
type NotificationType = Email | SMS;

const notify = (notification: NotificationType) => {
    if (notification.type === 'email') {
        console.log(`Sending email to ${notification.emailId}`);
    } else if (notification.type === 'sms') {
        console.log(`Sending SMS to ${notification.phoneNumber}`);
    }
}

const pick = <T>(items: T[], index: number): T | undefined => {
    return items[index];
}

const email = pick<NotificationType>([
    {type: 'email', emailId: 'test@test.com'},
    {type: 'sms', phoneNumber: '+1234567890'}
], 1);

console.log(email);