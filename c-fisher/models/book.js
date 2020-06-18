import {HTTP} from '../utils/http.js'
class BookModel extends HTTP{

  constructor(){
    super()
    this.url_prefix = 'book'
  }

  /**
   * 查询书籍详情
   * bookId:书本唯一标识
   */
  getDetail(bookId){
    return this.request({
      // url:this.url_prefix+'/detail/'+bookId
      url:`${this.url_prefix}/detail/${bookId}`
    })
  }

  getBook(bookId){
    return this.request({
      url:`${this.url_prefix}/${bookId}`
    })
  }
  
  /**
   * 搜索书籍
   * q:搜索关键字
   */
  search(q){
    return this.request({
      url:this.url_prefix+'/search',
      data:{q:q},
      method:'POST'
    })
  }

  /**
   * 将搜索关键字添加到缓存
   * q:搜索关键字
   */
  addSearchHistory(q){
    // 1，先从缓存获取
    let searchHistory = wx.getStorageSync('history_words') || []
    // 2，判断查询条件q 长度是否超过10
    if (searchHistory.length>=10){
      searchHistory.pop()
    }
    // 3，判断查询条件q 是否存在searchHistory
    if (searchHistory.indexOf(q) < 0){
      searchHistory.unshift(q)
    }
    // 4，加入到缓存中
    wx.setStorageSync('history_words', searchHistory)
    return searchHistory
  }
}

export {
  BookModel
}