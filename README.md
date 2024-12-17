<p align="center">
  <a href="">
    <img src="https://s32.picofile.com/file/8481356268/logo.png" />
  </a>
</p>

#

Stadino is a web application built using the Django framework that allows users to browse, search, and purchase books online. It provides a seamless shopping experience, featuring:

- **User Authentication :** Secure user registration and login

- **Product Catalog:** A comprehensive catalog of books with detailed descriptions and images.

- **Shopping Cart:** A robust shopping cart system for adding, removing, and modifying items.

- **Checkout Process:** A straightforward checkout process with payment integration.


## Tech Stack

[![My Skills](https://skillicons.dev/icons?i=js,html,css,django,python)](https://skillicons.dev)


## Installation on your system

1 . **Clone the Repository:**

```bash
    git clone https://github.com/MohsenSangSefidi/Stadino
```

2 . **Create a Virtual Environment:**

```bash
    python -m venv .venv
```

3 . **Activate the Virtual Environment:**

- Windows

    ```bash
        venv\Scripts\activate
    ```

- Linux/macOS

    ```bash
        source venv/bin/activate
    ```

4 . **Install Dependencies:**

```bash
    pip install -r requirements.txt
```

5 . **Configure the Database:**

- Create a postgersql database in your system.

- Update the DATABASE_URL setting in settings.py file.

6 . **Run Migrations:**

```bash
    python manage.py migrate
```

7 . **Start the Development Server:**

```bash
    python manage.py runserver
```

8 . **Usage:**

- Access the Website: Open your web browser and go to http://127.0.0.1:8000/.

- Explore the Catalog: Browse through different book categories and search for specific titles.

- Create an Account: Register a new account to start shopping.

- Add Items to Cart: Add books to your cart and proceed to checkout.

- Checkout and Payment: Complete the checkout process and make a secure payment.

## Contributing

I welcome contributions to Stadino! Please feel free to fork the repository and submit pull requests.


## License

This project is licensed under the MIT License.