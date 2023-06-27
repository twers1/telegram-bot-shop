# Online shop for the telegram bot

##### en

This telegram bot is needed in order to create your own store in the bot itself and start your business in the most popular messenger 

* Use python language, aiogram library, DB postgresql

## Functions: 

user_panel

    Catalog 
    Cart
    Contacts

The catalog contains a multi-level catalog that shows first the categories, then the products in that category, and then the product card. The product card has "Add to cart" and "Go to menu" buttons. Clicking on the button "Add to cart" adds to the cart itself, and shows new 2 buttons "+" and "-", clicking on the button "+" adds this same item by one unit, and when you click "-" does the same thing only removes one item from the database 

The cart contains the user's products, and also has "Checkout" and "Clear Cart" buttons, when you click on "Checkout" - the user must enter his data (phone number, delivery address, delivery method, method of payment, and so on). If you click "Clear cart" - the cart itself is cleared completely

The "Contacts" button stores information about the administrator himself 



admin_panel 

    Add category
    Add product
    Delete product
    Bank card details
    Prepayment amount

## Demo 

## Docker 

##### ru 

Данный телеграмм-бот нужен для того, чтобы создать свой собственный магазин и начать свой бизнес в самом популярном мессенджере. 

Технологии, которые использовались для создания этого бота: 
* язык программирования Python
* библиотека aiogram
* база данных Postgresql


## Функции бота

Для пользоваталей доступно: 

    Каталог
    Корзина 
    Контакты 

Каталог содержит в себе многоуровневый каталог, который показывает сначала категории товара, потом товары, которые есть в категории, а потом уже саму карточку товара. В карточке товара можно "Добавить в корзину" и "Перейти в меню". При нажатии кнопки "Добавить в корзину" - добавляется в корзину, а также отправляются еще 2 кнопки "+" и "-", нажимая на кнопку "+" добавляется одна единица товара, а при нажатии "-" убавляется одна единица товара 

Корзина содержит в себе товары, которые пользователь добавил в саму корзину

Контакты содержат в себе контакт администратора магазина

Для админов доступно: 

    Добавление категории
    Добавление товара 
    Удаление товара 
    Реквизиты банковской карты 
    Размер предоплаты 
    Выйти из админ-панели

## Демонстрация

## Docker

    