

class Pagination{
  static isCanLoadingMoreData(start,total) {
    if (start >= total) {
      return false
    }
    return true
  }
}

export {
  Pagination
}