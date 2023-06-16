import { date as quasardate } from 'quasar';

const formatDate = (date: string, format?: string) => {
  return quasardate.formatDate(date, format || 'YYYY-MM-DD HH:mm');
};

export { formatDate };
