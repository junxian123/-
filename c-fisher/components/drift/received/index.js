// components/drift/received/index.js
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
    onCancel(event){
      const did = event.currentTarget.dataset.id
      this.triggerEvent('cancel',{did:did})
    },
    
    onDelete(event){
      const did = event.currentTarget.dataset.id
      this.triggerEvent('delete', { did: did })
    }
  }
})
