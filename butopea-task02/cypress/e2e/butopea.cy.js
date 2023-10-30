describe("butopea test", () => {
  // visit https://butopea.com/ before each test
  beforeEach(() => {
    cy.visit("/");
  });

  it("square with text n button", () => {
    // find the first div with class banner-square-overlay-container
    cy.get("div.banner-square-overlay-container").within(() => {
      // find child p and button elements and allias their text values
      cy.get("p").invoke("text").as("text");
      cy.get("button").invoke("text").as("btnText");
    });

    // find all divs with class banner-square-image
    cy.get("div.banner-square-image")
      // take the second one
      .eq(1)
      // find child img element and allias its src value
      .within(() => {
        cy.get("img").invoke("attr", "src").as("imgLink");
      });

    // log the all the allias values
    cy.get("@text").then((text) => {
      cy.log("Text: " + text);
    });

    cy.get("@btnText").then((btnText) => {
      cy.log("Button text: " + btnText);
    });

    cy.get("@imgLink").then((imgLink) => {
      cy.log("Image link: " + Cypress.config().baseUrl + imgLink);
    });
  });

  it("products", () => {
    // find the button with text "Új termékek" and click it
    cy.get("button").contains("Új termékek").click();
    // find the div with id new-arrivals and allias its children
    cy.get("#new-arrivals > section > div > div").children().as("products");

    cy.get("@products").then((products) => {
      cy.log("Number of products: " + products.length);

      // iterate over the products
      products.each((index, product) => {
        // find the product name, price, link and image link and allias them
        cy.wrap(product).within(() => {
          cy.get(".product-tile-info").within(() => {
            cy.get("p").invoke("text").as("productName");
            cy.get("div").invoke("text").as("productPrice");
          });

          cy.get("a").eq(0).invoke("attr", "href").as("productLink");
          cy.get("img").eq(1).invoke("attr", "src").as("imgLink");
        });

        cy.get("@productName").then((productName) => {
          cy.log("Product name: " + productName);
        });

        cy.get("@productPrice").then((productPrice) => {
          cy.log("Product price: " + productPrice);
        });

        cy.get("@productLink").then((productLink) => {
          cy.log("Product link: " + Cypress.config().baseUrl + productLink);
        });

        cy.get("@imgLink").then((imgLink) => {
          cy.log("Image link: " + Cypress.config().baseUrl + imgLink);
        });
      });
    });
  });
});
