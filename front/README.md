# Domain expiration Bot. [FRONT]

## Файловая система
```
front/
├── public/
│   └── index.html
├── src/
│   ├── assets/                # картинки, шрифти, SCSS
│   │   └── styles/
│   │       └── main.scss
│   ├── components/            # багаторазові компоненти (Header, Sidebar, Card і т.д.)
│   ├── layouts/               # Layouts (AuthLayout, DashboardLayout)
│   ├── router/                # Vue Router (маршрутизація)
│   │   └── index.ts
│   ├── views/                 # повні сторінки (LoginView, DashboardView)
│   │   ├── auth/
│   │   │   └── LoginView.vue
│   │   └── dashboard/
│   │       └── DashboardView.vue
│   ├── store/                 # Pinia (auth store тощо)
│   │   └── auth.ts
│   ├── storage/
│   │   ├── modules/
│   │   │   ├── auth.ts        # токени, користувач, редіректи
│   │   │   └── ...            # інші
│   │   ├── types/
│   │   │   └── localStorage.ts # read/write/remove factory
│   │   └── index.ts           # збирає всі модулі
│   ├── api/                   # API-запити
│   │   └── auth.ts
│   ├── App.vue                # кореневий шаблон
│   └── main.ts                # точка входу
├── package.json
└── vite.config.ts

```