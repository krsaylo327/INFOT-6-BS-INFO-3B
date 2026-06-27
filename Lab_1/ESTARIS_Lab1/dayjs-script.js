const dayjs = require('dayjs');

const now = dayjs();

const readableNow = now.format('MMMM D, YYYY');

const nextWeek = now.add(7, 'day');

const readableNextWeek = nextWeek.format('MMMM D, YYYY');

console.log("Current Date:", readableNow);
console.log("Date Next Week:", readableNextWeek);

