const dayjs = require('dayjs');

const now = dayjs();

const formattedNow = now.format('MMMM D, YYYY');

const nextWeek = now.add(7, 'day');
const formattedNextWeek = nextWeek.format('MMMM D, YYYY');

console.log("Today is:", formattedNow);
console.log("Next week will be:", formattedNextWeek);
