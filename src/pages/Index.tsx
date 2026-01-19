import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import Icon from '@/components/ui/icon';

const Index = () => {
  const [openFaq, setOpenFaq] = useState<number | null>(null);
  const [formData, setFormData] = useState({ name: '', contact: '', project: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Спасибо, ${formData.name}! 🎉\n\nВаша заявка принята.\nОтвет пришлём в течение 24 часов.`);
    setFormData({ name: '', contact: '', project: '' });
  };

  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  const tools = [
    { name: 'Perplexity AI', logo: 'P', desc: 'Исследования и анализ' },
    { name: 'HeyGen', logo: 'HG', desc: 'ИИ-аватары и видео' },
    { name: 'Google NotebookLM', logo: 'NL', desc: 'Обработка текстов' },
    { name: 'Freepik', logo: 'F', desc: 'Генерация изображений' },
    { name: 'Nano Banana Pro', logo: 'NB', desc: 'Фотосессии продуктов' },
    { name: 'Kling 2.6', logo: 'K', desc: 'Видео высокого качества' }
  ];

  const services = [
    { icon: '✨', title: 'Продающие ИИ-лендинги', desc: 'Создаю одностраничные сайты под продажу услуг. Структура, тексты, визуал, подключение форм и аналитики — всё готово за 5–7 дней. Средняя конверсия: 5–12%.' },
    { icon: '📊', title: 'Презентации для бизнеса', desc: 'Делаю презентации для инвесторов, партнёров, клиентов. ИИ-дизайн + сторителлинг = убеждающая история. Форматы: PDF, видеопрезентация, интерактивная.' },
    { icon: '📈', title: 'Профессиональная инфографика', desc: 'Превращу сложные данные, процессы и услуги в понятные схемы. Используется в лендингах, контенте, обучении. Стиль под ваш бренд.' },
    { icon: '📸', title: 'ИИ-фотосессия для бизнеса', desc: 'Генерирую фирменные снимки: вас, команду, продукт с использованием Google Nano Banana Pro. Без реальной съёмки и фотографов. Экономия: в 5–10 раз дешевле.' },
    { icon: '🛍️', title: 'Карточки товаров для маркетплейсов', desc: 'Создаю визуалы товаров с ИИ, заголовки, описания и УТП. Работаю под Wildberries, Ozon, Яндекс.Маркет. Оптимизировано под поиск и CTR.' },
    { icon: '🎵', title: 'Песни и гимны компании', desc: 'Пишу и создаю фирменные треки, гимны, jingles для бренда. Используются в видео, ивентах, рекламе. Уникальный звуковой брендинг для вашего бизнеса.' },
    { icon: '✍️', title: 'Уникальные тексты + контент-план', desc: 'Создаю позиционирование, рубрики, 30–90-дневный контент-план и готовые тексты для Instagram, TikTok, Telegram. Каждый пост ориентирован на продажи.' },
    { icon: '🤖', title: 'ИИ-ассистент для бизнеса', desc: 'Настраиваю персонального ассистента, который отвечает на вопросы клиентов, даёт консультации, помогает менеджерам. Работает 24/7, экономит время на 30–50%.' },
    { icon: '👤', title: 'ИИ-аватар руководителя', desc: 'Создаю цифровой образ вас или сотрудника для видеообращений, обучающих курсов, прямых эфиров через HeyGen. Выглядит как настоящее видео.' },
    { icon: '🎬', title: 'Видео и промо-ролики с ИИ', desc: 'Пишу сценарий, генерирую кадры с помощью Kling 2.6, Freepik, делаю монтаж и озвучку. Реклама, которая конвертирует в 3–5 раз лучше.' }
  ];

  const benefits = [
    { icon: '⚡', title: 'Скорость', desc: 'Лендинг или видео готовы за дни, а не недели' },
    { icon: '💰', title: 'Экономия', desc: '5–10 раз дешевле, чем нанимать специалистов отдельно' },
    { icon: '🎯', title: 'Результат', desc: 'Каждый материал ориентирован на конверсию' },
    { icon: '🔄', title: 'Быстрые тесты', desc: 'Легко A/B-тестировать и менять подходы за часы' },
    { icon: '📊', title: 'По скрипту', desc: 'Каждый лендинг создаётся по проверенной схеме' },
    { icon: '🤝', title: 'Один исполнитель', desc: 'Не торгуетесь с дизайнером, видеографом и копирайтером' },
    { icon: '🚀', title: 'Передовые технологии', desc: 'Используем только актуальные ИИ-инструменты' },
    { icon: '🔒', title: 'Безопасность и права', desc: 'Полные коммерческие права на созданный контент' }
  ];

  const faqs = [
    { q: 'Лендинг на ИИ будет видно, что сгенерирован?', a: 'Нет. Я дорабатываю всё вручную, добавляю реальные кейсы и отзывы. Выглядит как работа дорогого дизайнера.' },
    { q: 'Что если мне не понравится на первом этапе?', a: 'На шаге "Концепция" вы смотрите макеты и тексты. Если не подходит, меняю подход, деньги не теряете.' },
    { q: 'Нужно ли мне иметь навыки маркетинга?', a: 'Нет. Я упаковываю всё под результат. Вы подготавливаете инфо о товаре/услуге, остальное — моё.' },
    { q: 'Видео на ИИ будет выглядеть по-робоцидному?', a: 'Если использую аватар через HeyGen — минимальный эффект "неестественности". Но с Kling 2.6 и хорошим сценарием выглядит как настоящее.' },
    { q: 'Через сколько вижу результаты?', a: 'Лендинг работает сразу после запуска. Заявки/продажи — через 2–3 недели, когда соберётся статистика.' },
    { q: 'Какие права у меня на созданный контент?', a: 'Все инструменты, которые я использую (Freepik, HeyGen, Kling), предоставляют полные коммерческие права. Вы владеете всем созданным контентом.' }
  ];

  return (
    <div className="min-h-screen bg-background">
      <a 
        href="https://t.me/Aginnvl_bot" 
        target="_blank" 
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 bg-[#0088cc] hover:bg-[#0077b3] text-white rounded-full p-4 shadow-2xl transition-all hover:scale-110 flex items-center justify-center group"
        title="Задать вопрос в Telegram"
      >
        <Icon name="MessageCircle" className="w-6 h-6" />
        <span className="absolute right-full mr-3 bg-gray-900 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          Есть вопросы? Напишите боту!
        </span>
      </a>
      <section className="relative overflow-hidden bg-gradient-to-br from-primary via-secondary to-accent text-white py-20 px-6">
        <div className="container max-w-4xl mx-auto text-center animate-fade-in">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            ИИ-маркетинг под ключ: от лендинга до видео, которые приносят клиентов
          </h1>
          <p className="text-lg md:text-xl mb-8 opacity-95 leading-relaxed">
            Создаю продающие лендинги, визуал, контент и видео с помощью нейросетей. Вы экономите месяцы работы и деньги на фрилансеров — я упаковываю всё под результат.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              className="bg-accent hover:bg-accent-hover text-white shadow-lg hover:shadow-xl transition-all hover:scale-105"
              onClick={() => scrollToSection('cta')}
            >
              Получить бесплатную консультацию
            </Button>
            <Button 
              size="lg" 
              variant="secondary" 
              className="bg-white text-primary hover:bg-muted"
              onClick={() => scrollToSection('services')}
            >
              Посмотреть услуги
            </Button>
          </div>
        </div>
      </section>

      <section className="py-16 px-6 bg-muted/30">
        <div className="container max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 animate-slide-up">
            Мы используем самые передовые нейросети и AI-инструменты
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8">
            {tools.map((tool, i) => (
              <Card key={i} className="p-6 text-center hover:shadow-lg transition-all hover:-translate-y-2 animate-scale-in" style={{ animationDelay: `${i * 100}ms` }}>
                <div className="w-16 h-16 mx-auto mb-3 bg-primary/10 rounded-xl flex items-center justify-center text-2xl font-bold text-primary">
                  {tool.logo}
                </div>
                <h3 className="font-semibold text-sm mb-1">{tool.name}</h3>
                <p className="text-xs text-muted-foreground">{tool.desc}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="container max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Вы можете: тратить месяцы и деньги ИЛИ запустить результаты за 2 недели
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <Card className="p-8 border-2 border-destructive/20 bg-destructive/5 animate-fade-in">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-2 text-destructive">
                <Icon name="X" className="w-6 h-6" /> Без ИИ
              </h3>
              <ul className="space-y-3">
                {['Нанимать разных специалистов', 'Ждать 2–4 недели на материалы', 'Тратить 200–500 тыс. ₽', 'Переделки каждые 2 недели', 'Нет гарантии на результат'].map((item, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <Icon name="X" className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </Card>

            <Card className="p-8 border-2 border-green-500/20 bg-green-50 animate-fade-in" style={{ animationDelay: '200ms' }}>
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-2 text-green-600">
                <Icon name="Check" className="w-6 h-6" /> С ИИ-маркетингом
              </h3>
              <ul className="space-y-3">
                {['Один исполнитель, который разбирается во всём', 'Лендинг за 5–7 дней', 'От 50 тыс. ₽ за комплекс', 'Быстрые итерации и улучшения', 'Структура, которая конвертирует'].map((item, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <Icon name="Check" className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        </div>
      </section>

      <section id="services" className="py-16 px-6 bg-muted/30">
        <div className="container max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Что я делаю с ИИ для вашего бизнеса
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service, i) => (
              <Card key={i} className="p-6 hover:shadow-xl transition-all hover:-translate-y-2 animate-scale-in" style={{ animationDelay: `${i * 50}ms` }}>
                <div className="text-4xl mb-4">{service.icon}</div>
                <h3 className="text-lg font-bold mb-3">{service.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{service.desc}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="container max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Процесс работы: от идеи к результату за 10–14 дней
          </h2>
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { num: 1, title: 'Диагностика', desc: 'Разбираю вашу нишу, продукты, ставлю метрики (заявки, продажи, узнаваемость). Согласуем задачу и услуги.' },
              { num: 2, title: 'Концепция', desc: 'Создаю структуру лендинга или контент-план, предлагаю визуальный стиль, пишу тексты и УТП. Вы даёте обратную связь.' },
              { num: 3, title: 'Производство', desc: 'Генерирую всё на ИИ: визуал, видео, аватары, тексты, музыку. Дорабатываю вручную, адаптирую под платформы.' },
              { num: 4, title: 'Запуск', desc: 'Внедряю лендинг, подключаю аналитику, трекеры. Помогаю с изменениями и рекомендациями по A/B-тестированию.' }
            ].map((step, i) => (
              <div key={i} className="relative text-center animate-slide-up" style={{ animationDelay: `${i * 100}ms` }}>
                <div className="w-16 h-16 mx-auto mb-4 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold shadow-lg">
                  {step.num}
                </div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-sm text-muted-foreground">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-6 bg-muted/30">
        <div className="container max-w-5xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Почему клиенты выбирают именно ИИ-маркетинг
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {benefits.map((benefit, i) => (
              <div key={i} className="flex gap-4 animate-fade-in" style={{ animationDelay: `${i * 80}ms` }}>
                <div className="text-3xl flex-shrink-0">{benefit.icon}</div>
                <div>
                  <h3 className="font-bold mb-1">{benefit.title}</h3>
                  <p className="text-sm text-muted-foreground">{benefit.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="container max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
            Форматы сотрудничества и цены
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-lg">
              <thead>
                <tr className="bg-primary text-white">
                  <th className="p-4 text-left font-semibold">Пакет</th>
                  <th className="p-4 text-left font-semibold">Для кого</th>
                  <th className="p-4 text-left font-semibold">Включает</th>
                  <th className="p-4 text-left font-semibold">Срок</th>
                  <th className="p-4 text-left font-semibold">Цена</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { name: 'СТАРТ', target: 'Новички, MVP, тест', includes: '1 лендинг ИЛИ контент-план + базовая инфографика', duration: '7 дней', price: 'от 30 тыс. ₽' },
                  { name: 'БИЗНЕС', target: 'Действующие проекты', includes: 'Лендинг + контент-план + ИИ-видео (3 шт) + инфографика', duration: '10 дней', price: 'от 75 тыс. ₽' },
                  { name: 'ПРО', target: 'Масштаб, комплекс', includes: 'Всё выше + ИИ-фотосессия + карточки товаров + ассистент', duration: '14 дней', price: 'от 150 тыс. ₽' },
                  { name: 'ПРЕМИУМ', target: 'Full-cycle', includes: 'Полный пакет: лендинг + контент + видео + инфографика + фото + карточки + ассистент + аватар + песня', duration: '21 день', price: 'от 300 тыс. ₽' }
                ].map((pkg, i) => (
                  <tr key={i} className="border-b hover:bg-muted/50 transition-colors">
                    <td className="p-4 font-bold">{pkg.name}</td>
                    <td className="p-4 text-sm">{pkg.target}</td>
                    <td className="p-4 text-sm">{pkg.includes}</td>
                    <td className="p-4 text-sm">{pkg.duration}</td>
                    <td className="p-4 font-bold text-primary">{pkg.price}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="py-16 px-6 bg-muted/30">
        <div className="container max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-8">
            Кто я и почему вам доверить проект
          </h2>
          <div className="space-y-4 mb-12 text-muted-foreground">
            <p>5+ лет в интернет-маркетинге. Специалист в ИИ-инструментах для создания лендингов, видео, дизайна и музыки.</p>
            <p>Запустил 50+ успешных проектов. Средняя конверсия лендингов: 7–12%. Работал с агентствами и напрямую с владельцами бизнеса.</p>
            <p>Постоянно учусь новым ИИ-инструментам (Perplexity, Freepik, Kling 2.6, Google NotebookLM) и применяю их на практике.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { text: 'Сделал лендинг, который кликают в 10 раз чаще, чем я ожидал', author: 'Дмитрий', role: 'владелец e-commerce' },
              { text: 'Контент-план спас мой Instagram, теперь продаю из соцсетей', author: 'Елена', role: 'SMM-менеджер' },
              { text: 'Видео на ИИ выглядит лучше, чем профессиональная съёмка', author: 'Александр', role: 'маркетолог' }
            ].map((testimonial, i) => (
              <Card key={i} className="p-6 border-l-4 border-l-primary animate-fade-in" style={{ animationDelay: `${i * 150}ms` }}>
                <p className="text-sm italic mb-4">&ldquo;{testimonial.text}&rdquo;</p>
                <p className="text-sm font-semibold">{testimonial.author}</p>
                <p className="text-xs text-muted-foreground">{testimonial.role}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="container max-w-3xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Часто спрашивают</h2>
          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <Card key={i} className="overflow-hidden animate-scale-in" style={{ animationDelay: `${i * 80}ms` }}>
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full p-6 text-left flex justify-between items-center hover:bg-muted/50 transition-colors"
                >
                  <span className="font-semibold pr-4">В: {faq.q}</span>
                  <Icon name={openFaq === i ? 'ChevronUp' : 'ChevronDown'} className="w-5 h-5 flex-shrink-0" />
                </button>
                {openFaq === i && (
                  <div className="px-6 pb-6 text-sm text-muted-foreground border-l-4 border-l-primary ml-6">
                    О: {faq.a}
                  </div>
                )}
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section id="cta" className="py-20 px-6 bg-muted/30">
        <div className="container max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Готовы запустить проект, который будет приносить клиентов?
          </h2>
          <p className="text-lg text-muted-foreground mb-8">
            Оставьте контакт — сделаю бесплатный аудит вашей ниши и пришлю план работ.
          </p>
          <Card className="p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="text-left">
                <label className="block text-sm font-semibold mb-2">Ваше имя</label>
                <Input
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Ваше имя"
                />
              </div>
              <div className="text-left">
                <label className="block text-sm font-semibold mb-2">Телефон / WhatsApp / Telegram</label>
                <Input
                  required
                  value={formData.contact}
                  onChange={(e) => setFormData({ ...formData, contact: e.target.value })}
                  placeholder="Ваш контакт"
                />
              </div>
              <div className="text-left">
                <label className="block text-sm font-semibold mb-2">Коротко о вашем проекте</label>
                <Textarea
                  required
                  rows={4}
                  value={formData.project}
                  onChange={(e) => setFormData({ ...formData, project: e.target.value })}
                  placeholder="Расскажите о вашем проекте"
                />
              </div>
              <Button type="submit" size="lg" className="w-full bg-accent hover:bg-accent-hover">
                Отправить заявку
              </Button>
              <p className="text-xs text-muted-foreground">
                Ответ в течение 24 часов. Мы не спамим и не продаём контакты.
              </p>
            </form>
          </Card>
        </div>
      </section>

      <footer className="bg-dark text-white py-12 px-6">
        <div className="container max-w-5xl mx-auto text-center">
          <p className="mb-4">&copy; 2026 ИИ-Маркетинг. Все права защищены.</p>
          <div className="flex flex-wrap justify-center gap-6 text-sm mb-4">
            <button onClick={() => scrollToSection('services')} className="hover:opacity-80 transition-opacity">Услуги</button>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="hover:opacity-80 transition-opacity">Instagram</a>
            <a href="https://telegram.me" target="_blank" rel="noopener noreferrer" className="hover:opacity-80 transition-opacity">Telegram</a>
            <a href="mailto:hello@example.com" className="hover:opacity-80 transition-opacity">Email</a>
            <a href="#privacy" className="hover:opacity-80 transition-opacity">Политика конфиденциальности</a>
          </div>
          <p className="text-xs opacity-80">Владивосток, Приморье, РФ</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;