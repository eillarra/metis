import { iconStep1, iconStep2, iconStep3, iconStep4, iconStep5, iconStepFinal } from '@/icons';

const getEvaluationSteps = (internship: Internship, isSelf?: boolean) => {
  const evaluationSteps = [];

  for (const tag of internship.tags) {
    if (tag.startsWith('intermediate.') && tag.includes('.self:') === (isSelf || false)) {
      const simpleTag = isSelf ? tag.replace('.self:', ':') : tag;
      const [number, status] = simpleTag.substring(13).split(':');
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
        icon:
          number == '0'
            ? iconStepFinal
            : {
                '1': iconStep1,
                '2': iconStep2,
                '3': iconStep3,
                '4': iconStep4,
                '5': iconStep5,
              }[number],
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
