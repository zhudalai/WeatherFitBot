import React from 'react';
import type { OutfitAdvice } from '../types';
import type { Lang } from '../i18n';
import { t } from '../i18n';

interface OutfitCardProps {
  advice: OutfitAdvice;
  lang?: Lang;
}

const OutfitCard: React.FC<OutfitCardProps> = ({ advice, lang = "zh" }) => {
  return (
    <div className="rounded-xl bg-gradient-to-br from-amber-50 to-orange-100 p-4 shadow-sm">
      <h4 className="mb-2 text-base font-semibold text-gray-800">👔 {t(lang, 'outfitAdvice')}</h4>
      <p className="mb-3 text-sm text-gray-700">{advice.summary}</p>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div className="rounded-lg bg-white/60 p-2">
          <span className="font-medium text-gray-700">👆 {t(lang, 'top')}：</span>
          <span className="text-gray-600">{advice.top}</span>
        </div>
        <div className="rounded-lg bg-white/60 p-2">
          <span className="font-medium text-gray-700">👇 {t(lang, 'bottom')}：</span>
          <span className="text-gray-600">{advice.bottom}</span>
        </div>
        <div className="rounded-lg bg-white/60 p-2">
          <span className="font-medium text-gray-700">👟 {t(lang, 'shoes')}：</span>
          <span className="text-gray-600">{advice.shoes}</span>
        </div>
        <div className="rounded-lg bg-white/60 p-2">
          <span className="font-medium text-gray-700">🎒 {t(lang, 'accessories')}：</span>
          <span className="text-gray-600">{advice.accessories}</span>
        </div>
      </div>
      {advice.tips && (
        <p className="mt-3 rounded-lg bg-yellow-100/80 p-2 text-sm text-yellow-800">
          💡 {advice.tips}
        </p>
      )}
    </div>
  );
};

export default OutfitCard;
