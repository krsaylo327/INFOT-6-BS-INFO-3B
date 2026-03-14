const dayjs = require ('dayjs');
const now = dayjs();
const today = now.format('YYYY-MM-DD');
console.log(today);
console.log('Date Next week:', now.add(7, 'day').format('YYYY-MM-DD'));

