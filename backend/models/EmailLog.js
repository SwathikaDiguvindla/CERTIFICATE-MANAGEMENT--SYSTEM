class EmailLog {
    constructor(id, student_id, status, sent_time) {
        this.id = id;
        this.student_id = student_id;
        this.status = status;
        this.sent_time = sent_time;
    }
}

module.exports = EmailLog;