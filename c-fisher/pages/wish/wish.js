import {WishModel} from '../../models/wish.js'
const wishModel = new WishModel()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    wishes: null,
    loading:false
  },

  onShow: function () {
    this._setWishesOfSelf()
  },

  _setWishesOfSelf() {
    this._loadingShow()
    wishModel.getWishesOfSelf().then(res => {
      this._loadingHide()
      this.setData({
        wishes: res
      })
    })
  },

  onDetail(event){
    const bookId = event.target.dataset.id
    console.log(event)
    wx.navigateTo({
      url: '/pages/book-detail/book-detail?bookId='+bookId,
    })
  },

  onCancel(event){
    const bookId = event.target.dataset.id
    let wishes = this.data.wishes
    wishModel.cancel(bookId).then(res=>{
      wishModel.update(wishes,bookId)
      this.setData({
        wishes:wishes
      })
    })
  },

  toIndexPage() {
    wx.switchTab({
      url: '/pages/index/index',
    })
  },

  _loadingShow() {
    this.setData({
      loading: true
    })
  },

  _loadingHide() {
    this.setData({
      loading: false
    })
  }
})