class Game {
    constructor() {
        this.words = new Set();
        this.score = 0;
        this.secs = 60;

        this.timer = setInterval(this.timerTick.bind(this), 1000);

        $("#guess-form").on("submit", this.submitGuess.bind(this));

    }

    async submitGuess(evt) {
        evt.preventDefault();
        let $guess = $('.guess-input').val();

        const res = await axios.get('/submit-guess', { params: {guess: $guess} });
        console.log(res);
        if (res.data.result === 'ok') {
            this.words.add($guess);
            this.updateWords($guess);
            this.score += $guess.length;
            this.updateScore();
            this.showMessage(`Added ${$guess}!`, 'success');
        } 
        else if (res.data.result === 'not-word') {
            this.showMessage(`${$guess} is not a word`, 'fail');
        } 
        else if (res.data.result === 'not-on-board') {
            this.showMessage(`${$guess} is not on the board`, 'fail');
        }

        $('.guess-input').val('').focus();
    }

    showMessage(msg, cls) {
        $('#message').text(msg).removeClass().addClass(cls);
    }

    updateTimer() {
        $('#timer-display').text(this.secs);
    }

    async timerTick() {
        this.secs -= 1;
        this.updateTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            this.trackScore();
        }
    }

    updateWords(word) {
        $('#words').append(`<li>${word}</li>`);
    }

    updateScore() {
        $('.score').text(this.score);
    }

    async trackScore() {
        $("#guess-form").hide();
        const res = await axios.post('/track-score', {score: this.score});
        if(res.data.newRecord) {
            this.showMessage(`${this.score} is a new record!`, 'record');
        } else {
            this.showMessage(`Final Score: ${this.score}`, 'final');
        }
    }

}

