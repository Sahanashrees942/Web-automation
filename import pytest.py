import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.tests
def test():
        playwright= sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")
        page.wait_for_timeout(5000)
        page.locator("[data-test=\"username\"]").click()
        page.wait_for_timeout(5000)
        page.fill("[data-test=\"username\"]","standard_user")
        page.wait_for_timeout(5000)
        page.locator("[data-test=\"password\"]").click()
        page.wait_for_timeout(5000)
        page.fill("[data-test=\"password\"]","secret_sauce")
        page.wait_for_timeout(5000)
        page.click("[data-test=\"login-button\"]")
        page.wait_for_timeout(5000)

        #Verify that successful login will land the user on Products page
        page.wait_for_selector("[data-test='inventory-container']")
        page.wait_for_timeout(5000)
        title = page.locator("[data-test='title']").text_content()
        page.wait_for_timeout(5000)

        assert title == "Products", f"Expected 'Products' but got '{title}'"

        #Get the first product item name and price, store it in a text file
        product_name = page.locator("#item_4_title_link > div").first.text_content()
        page.wait_for_timeout(5000)
        product_price = page.locator("[data-test=\"inventory-item-price\"]").first.text_content()
        page.wait_for_timeout(5000)

        # Save the product name and price to a text file
        with open("product_info.txt", "w") as file:
                file.write(f"Product Name: {product_name}\n")
                file.write(f"Product Price: {product_price}\n")

        page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
        page.wait_for_timeout(5000)
        page.locator("[data-test=\"shopping-cart-link\"]").click()
        page.wait_for_timeout(5000)

        cart_product_name = page.locator("[class='inventory_item_name']").first.text_content()
        cart_product_price = page.locator("[class='inventory_item_price']").first.text_content()

        # Verify if the product in the cart matches the product added
        assert product_name.strip() == cart_product_name.strip(), f"Expected product name '{product_name}', but got '{cart_product_name}'"
        assert product_price.strip() == cart_product_price.strip(), f"Expected product price '{product_price}', but got '{cart_product_price}'"

        page.get_by_role("button", name="Open Menu").click()
        page.locator("[data-test=\"logout-sidebar-link\"]").click()

        # ---------------------
        page.close()
        context.close()
        browser.close()
        playwright.stop()