const config = {
  url_prefix: 'http://localhost:5000/v1/'
}

const tips = {
  1: '抱歉！出现了一个错误',
  80010: '没有找到相关图书',
  10040: '令牌失效',
  10050: '令牌过期'
}

// 分页开始索引号增加步伐
const start_step = 8


export {
  config,
  tips,
  start_step
}