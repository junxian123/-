class BookViewModel{

  constructor(book){
    this.id = book.id
    this.author = book.author
    this.title = book.title
    this.image = book.image
  }
}

export {
  BookViewModel
}