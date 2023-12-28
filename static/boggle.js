//contains classes to manage the data of the app and the connection to the API.
class BoggleGame {
    /* make a new game at this DOM id */
  
    constructor(boardId, secs=60) {
      this.words = new Set();
      this.board = $("#" + boardId);
        // post a score
      this.score = 0;
        //add a timer
      this.secs = secs;
      this.showTimer();

      //show visual passage of time
      this.timer = setInterval(this.passage.bind(this),1000);

      $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }
  
    //show word on front end --- add to a list and append 
  
    showWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    }

    // show score
    showScore(){
      $(".score", this.board).text(this.score);
    }
  
    // show a submission status message --how will the code's response.data.result display on front end?
    
    showStatus(msg){
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
        this.showStatus(`Already found ${word}.`);
        return;
      }
  
      // check server for validity
      const resp = await axios.get("/check-word", { params: { word: word }});
      if (resp.data.result === "not-word") {
        
        //show a front end message
        this.showStatus(`${word} is not a valid English word`);
  
      } else if (resp.data.result === "not-on-board") {
        this.showStatus(`${word} is not a a valid word on this board.`);
    
      } else {
        this.showWord(word);
        this.showStatus(`Added: ${word}.`);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
      }
  
      $word.val("").focus();
    }
    //Timer--
    showTimer(){
      $(".timer", this.board).text(this.secs);
    }

    //show the passage of time in increments of one second visually on the game
    async passage(){
      this.secs -=1;
      this.showTimer();
      //NEED TO STOP TIMER AT O
      if(this.secs === 0){
        clearInterval(this.timer);
        await this.finalScore();
      }
    }
    
    //end of game - final score
    async finalScore(){
      $(".add-word", this.board).hide();
      $(".STBOARD", this.board).hide();
      this.showStatus(`your final score is: ${this.score}`);
    }
  }
  
