import {BookModel} from '../../models/book.js'
import {GiftModel} from '../../models/gift.js'
import {WishModel} from '../../models/wish.js'
import {DriftModel} from '../../models/drift.js'
import {BookViewModel} from '../../view_models/book.js'
import {DriftViewModel} from '../../view_models/drift.js'

const bookModel = new BookModel()
const giftModel = new GiftModel()
const wishModel = new WishModel()
const driftModel = new DriftModel()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    book: null,
    bookId: null,
    wished: null,
    gifted: null,
    wishId: null,

    isShowPopup: false,
    isShowDriftPopup: false,
    isGifter: false,
    isWisher: false,
    loading:false,

    giftText: '赠送此书',
    wishText: '加入到心愿清单',
    saveOfGiftText: '已添加至赠送清单',
    saveOfWishText: '已添加至心愿清单',

    tradeGiftsTitle: '向他们赠送此书',
    tradeWishesTitle: '向他们请求此书',
    requestText: '向他请求图书',
    responseText: '向他赠送图书',
    requestedText: '已向他请求图书',
    responsedText: '已向他赠送图书'

  },
  onShow:function(){
    this._getDetail(this.data.bookId)
  },

  onLoad: function (options) {
    const bookId = options.bookId
    this.data.bookId = bookId
  },

  _getDetail(bookId) {
    this._loadingShow()
    bookModel.getDetail(bookId).then(res => {
      this._loadingHide()
      this.setData({
        isGifter: res.is_gifter,
        isWisher: res.is_wisher,
        book: res.book,
        wished: res.wished,
        gifted: res.gifted
      })
    })
  },

  onWish(event){
    const bookId= this.data.bookId
    wishModel.save_of_wish(bookId).then(res=>this._getDetail(bookId))
  },

  sendDrift(event){
    // 向他赠送此书，保存书籍信息、赠送者信息不包含邮寄信息，发送鱼漂，等待对方接受。
    const wishId = this.data.wishId
    const bookViewModel = new BookViewModel(this.data.book)
    const driftViewModel = new DriftViewModel({
      book:bookViewModel, wishId:wishId
      })
    driftModel.sendDriftOfGift(driftViewModel).then(res=>{
      this._getDetail(this.data.bookId)
      this.onExitPopup()
    })
  },

  onRequest(event){
    // 如果是心愿者，跳转到发送鱼漂页面，填写完整邮寄信息，发送鱼漂，向他请求此书。
    const giftId = event.target.dataset.id
    const bookId = this.data.bookId
    wx.navigateTo({
      url: '/pages/write-drift/write-drift?giftId='+giftId+'&bookId='+bookId,
    })
  },

  onGift(event){
    const bookId = this.data.bookId
    giftModel.save_of_gift(bookId).then(res=>{
      this._getDetail(bookId)
      this.onExitPopup()
    })
  },

  onShowDriftPopup(event){
    this.data.wishId = event.target.dataset.id
    this.setData({ isShowDriftPopup: true })
  },

  onShowPopup(event){
    this.setData({isShowPopup: true})
  },

  onExitPopup(event){
    this.setData({ 
      isShowPopup: false,
      isShowDriftPopup:false
    })
  },

  _loadingShow(){
    this.setData({loading:true})
  },

  _loadingHide(){
    this.setData({loading:false})
  }
})