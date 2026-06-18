class Certificate {
    constructor(id, student_id, certificate_id, pdf_path, qr_path, created_at) {
        this.id = id;
        this.student_id = student_id;
        this.certificate_id = certificate_id;
        this.pdf_path = pdf_path;
        this.qr_path = qr_path;
        this.created_at = created_at;
    }
}

module.exports = Certificate;