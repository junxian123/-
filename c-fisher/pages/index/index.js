import {BookModel} from '../../models/book.js'
import {GiftModel} from '../../models/gift.js'
import {start_step} from '../../config.js'
import {Pagination} from '../../utils/pagination.js'

const bookModel = new BookModel()
const giftModel = new GiftModel()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isShowSearchUI: false,
    isShowSearchResult: false,
    isShowLoading: false,
    isShowLoadingMore: false,
    isShowEndingMore: false,

    start :0,
    recentlyUploadedTotal : 0,
    searchTotal : 0,
    q:'',

    searchResult: null,
    recentlyUploaded: [],

    searchHistory: [],

    placeholder:'标题、ISBN',
  },

  onLoad: function (options) {
    this._setRecentlyUploadedResult()
  },

  onReachBottom: function(event){
    const isShowSearchUI = this.data.isShowSearchUI
    if(isShowSearchUI) return 
   
    this.data.start += start_step
    const start = this.data.start
    const total = this.data.recentlyUploadedTotal
    const isCanLoadingMoreData = Pagination.isCanLoadingMoreData(start, total)

    if (!isCanLoadingMoreData){
      this.setData({ isShowEndingMore:true})
    }else{
      // 能加载更多数据
      this._loadingMoreShow()
      this._setRecentlyUploadedResult()
    }
  },

  onTag(event){
    const q = event.detail.q
    this._setSearchResult(q)
  },

  onConfirm(event){
    const q = event.detail.detail.value
    this._setSearchResult(q)
  },

  onCancel(){
    this.setData({
      isShowSearchUI: false,
      q:'',
      searchResult:[],
      isShowSearchResult: false
    })
  },

  onClear(){
    this.setData({
      isShowSearchResult:false,
      searchResult:[]
    })
  },

  onSearch(){
    this.setData({ isShowEndingMore: false })

    const history_words = wx.getStorageSync('history_words')||[]
    this.setData({
      isShowSearchUI:true,
      searchHistory: history_words
    })
  },

  _setRecentlyUploadedResult(){
    const start = this.data.start
    giftModel.getRecentlyUploaded(start).then(res => {
      const recentlyUploaded = this.data.recentlyUploaded.concat(res.books)
      this.setData({
        recentlyUploaded: recentlyUploaded,
        recentlyUploadedTotal:res.total
      })
      this._loadingMoreHide()
    })
  },

  _setSearchResult(q){
    this._loadingShow()
    bookModel.search(q).then(res => {
      console.log(q)
      this.setData({
        q:q,
        isShowSearchResult: true,
        searchHistory: bookModel.addSearchHistory(q), // 把查询条件添加到缓存（最多10条)
        searchResult: res,
      })
      this._loadingHide()
    }).catch(() => {
      this.setData({
        searchResult:[]
      })
      this._loadingHide()
    })
  },
  

  _loadingMoreShow(){
    this.setData({
      isShowLoadingMore:true
    })
  },

  _loadingMoreHide(){
    this.setData({
      isShowLoadingMore:false
    })
  },

  _loadingShow(){
    this.setData({
      isShowLoading:true,
      searchResult: [],
      searchHistory:[]
    })
  },

  _loadingHide(){
    this.setData({
      isShowLoading: false
    })
  },
})