import {GiftModel} from '../../models/gift.js'
const giftModel = new GiftModel()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    gifts: null,
    loading:false
  },

  onShow: function (options) {
   this._setGiftsOfSelf()
  },

  _setGiftsOfSelf() {
    this._loadingShow()
    giftModel.getGiftsOfSelf().then(res => {
      this._loadingHide()
      this.setData({
        gifts: res
      })
    })
  },

  onDetail(event){
    const bookId= event.target.dataset.id
    wx.navigateTo({
      url: '/pages/book-detail/book-detail?bookId=' + bookId,
    })
  },

  onCancel(event){
    const bookId = event.target.dataset.id
    let gifts = this.data.gifts
    giftModel.cancel(bookId).then(res=>{
      giftModel.update(gifts,bookId)
      this.setData({
        gifts:gifts
      })
    })
  },

  toIndexPage(event){
    wx.switchTab({
      url: '/pages/index/index',
    })
  },

  _loadingShow(){
    this.setData({
      loading:true
    })
  },

  _loadingHide(){
    this.setData({
      loading:false
    })
  }
})