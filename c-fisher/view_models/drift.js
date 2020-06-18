class DriftViewModel {
  constructor({giftId=null,driftId=null, wishId=null, book=null, mail=null, message=null}) {
    this.book = book
    this.wish_id = wishId
    this.gift_id = giftId
    this.drift_id = driftId
    this.mail = mail
    this.message = message
  }
}


export {
  DriftViewModel
}