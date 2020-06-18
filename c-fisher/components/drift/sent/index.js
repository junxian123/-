// components/drift/send/index.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    drift:Object
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
    onMail(event){
      const did = event.currentTarget.dataset.id
      this.triggerEvent('mail',{did:did})
    },

    onReject(event){
      const did = event.currentTarget.dataset.id
      this.triggerEvent('reject',{did:did})
    },
  }
})
