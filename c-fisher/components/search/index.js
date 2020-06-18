// components/search/index.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    searchHistory:Array
  },

  /**
   * 组件的初始数据
   */
  data: {

  },

  /**
   * 组件的方法列表
   */
  methods: {
    onTap(event){
      const q = event.detail.name
      this.triggerEvent('tag',{q:q})
    }
  }
})
