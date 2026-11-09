# Новая структура сайта INORI

```
/ (EN)  ·  /he/ (HE, RTL)
│
├── Home
├── Product: Digital Payment Note (DPN)
│   ├── How it works
│   ├── For payers
│   ├── For suppliers
│   └── Security & compliance
├── Solutions
│   ├── Businesses & corporates
│   ├── Government & public sector
│   └── Banks & fintech platforms   (бывшая Collaborations)
├── Services
│   ├── Regulatory & licensing support
│   ├── Financial process optimization
│   └── Implementation & integration
├── Technology   (Hyperledger Iroha + Soramitsu)
├── Company
│   ├── About
│   ├── Team & Board
│   ├── Partners
│   ├── Press
│   └── Careers (опционально)
├── Resources
│   ├── News & Insights
│   ├── Videos
│   └── FAQ
├── Contact / Get started
└── Legal: Terms · Privacy · Cookies · Accessibility · Regulatory info
```

**Меню:** Product · Solutions · Services · Company · Resources · Contact + кнопка **Get started** + EN/HE.

## Страница DPN — текущий этап
- Кнопка **«Watch video»** со ссылкой на текущее видео.
- Плейсхолдеры (мокапы ноутбука/телефона) под скриншоты платформы — скрины будут позже.

## Главная — блоки
1. Hero + CTA (Get started / How DPN works)
2. Trust bar: лицензия CMA, Soramitsu, СМИ
3. Проблема → решение
4. How it works (3–4 шага)
5. Для кого (бизнес / госсектор / банки)
6. Услуги (3 карточки)
7. Почему INORI (4 принципа)
8. Цифры / кейсы
9. Пресса и видео
10. FAQ (аккордеон)
11. Финальный CTA + форма

## Функционал

**MVP**
- Единая форма с типом запроса (бизнес / поставщик / банк / госорган / другое) → маршрутизация, согласие с Privacy, thank-you page
- WhatsApp, click-to-call
- HE (RTL) + EN, английские слаги
- Cookie consent, виджет доступности
- 301-редиректы со старых URL
- GA4 + цели на формы
- SEO: meta, OG, sitemap, schema.org (Organization, FAQ)

**Фаза 2**
- Блог / новости (CMS)
- Интерактивная схема DPN / калькулятор для поставщика
- Кейсы
- Lead magnets (one-pager, презентация)
- Логин в платформу DPN (если есть веб-кабинет)

## Редиректы

| Старый URL | Новый URL |
|---|---|
| /en/אודות/ | /en/company/about/ |
| /en/board/ | /en/company/team/ |
| /en/שיתופי-פעולה/ | /en/solutions/banks-fintech/ |
| /en/צור-קשר/ | /en/contact/ |
| /en/תקנון-אתר/ | /en/legal/terms/ |
| /en/privacy-policy/ | /en/legal/privacy/ |
| MP4 «Digital Payment Note» | /en/product/dpn/ |
