//contains classes to manage the data of the app and the connection to the API.
class BoggleGame {
    /* make a new game at this DOM id */
  
    constructor(boardId) {


      this.words = new Set();
      this.board = $("#" + boardId);

      $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
  
    /* show word in list of words */
  
    showWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    }
        /* show a status message */
  
    /* show a submission status message --how will the code's response.data.result display on front end?*/
    
    displayMessage(msg){
        $(".msg", this.board)
            .text(msg);
        }
    
  
    /* handle submission of word: if unique and valid, score & show */
  
    async handleSubmit(evt) {
      evt.preventDefault();
      const $word = $(".word", this.board);
  
      let word = $word.val();
      if (!word) return;
  
      if (this.words.has(word)) {
        this.displayMessage(`Already found ${word}.`);
        return;
      }
  
      // check server for validity
      const resp = await axios.get("/check-word", { params: { word: word }});
      if (resp.data.result === "not-word") {
        
        //show a front end message
        this.displayMessage(`${word} is not a valid English word`);
  
      } else if (resp.data.result === "not-on-board") {
        this.displayMessage(`${word} is not a a valid word on this board.`);
    
      } else {
        this.showWord(word);
        this.displayMessage(`Added: ${word}.`);
      }
  
      $word.val("").focus();
    }
  }
  