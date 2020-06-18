// components/avatar/index.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    text:String,
    grade:Number,
    openData:Boolean,
	receiveCount:Number,
	sendCount:Number
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
    getUserInfo(event){
      this.triggerEvent('getUserInfo', event.detail)
    },

  }
})
