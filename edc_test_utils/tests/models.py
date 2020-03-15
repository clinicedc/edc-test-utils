from edc_model.models import BaseUuidModel, HistoricalRecords


class SubjectConsent(BaseUuidModel):
    history = HistoricalRecords()


class SubjectReconsent(BaseUuidModel):
    history = HistoricalRecords()


class SubjectVisit(BaseUuidModel):
    history = HistoricalRecords()


class SubjectRequisition(BaseUuidModel):
    history = HistoricalRecords()
