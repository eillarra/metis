const getEvaluationSteps = (internship: Internship) => {
  const evaluationSteps = [];

  for (const tag of internship.tags) {
    if (tag.startsWith('intermediate.')) {
      const [number, status] = tag.substring(13).split(':');
      let color = '';

      if (status === 'approved') {
        color = 'dark';
      } else if (status === 'not_approved') {
        color = 'orange-8';
      } else if (status === 'pending') {
        color = 'grey-4';
      }

      // add the icon and color to the array
      evaluationSteps.push({
        number: number,
        icon: number == '0' ? 'library_add_check' : `filter_${number}`,
        color: color,
      });
    }
  }

  evaluationSteps.sort((a, b) => {
    if (a.number === '0') {
      return 1;
    }
    if (b.number === '0') {
      return -1;
    }
    return parseInt(a.number) - parseInt(b.number);
  });

  return evaluationSteps;
};

export { getEvaluationSteps };
