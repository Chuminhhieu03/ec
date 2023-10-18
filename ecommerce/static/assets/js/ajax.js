
const select = (el, all = false) => {
  el = el.trim();
  if (all) {
    return [...document.querySelectorAll(el)];
  } else {
    return document.querySelector(el);
  }
};

const on = (type, el, listener, all = false) => {
  let selectEl = select(el, all);
  if (selectEl) {
    if (all) {
      selectEl.forEach((e) => e.addEventListener(type, listener));
    } else {
      selectEl.addEventListener(type, listener);
    }
  }
};

function filterProduct() {
  let portfolioContainer = select(".portfolio-container");
  console.log("CMH");
  if (portfolioContainer) {
    let portfolioIsotope = new Isotope(portfolioContainer, {
      itemSelector: ".portfolio-item",
      layoutMode: "fitRows",
    });

    let portfolioFilters = select("#portfolio-flters li", true);

    on(
      "click",
      "#portfolio-flters li",
      function (e) {
        e.preventDefault();
        portfolioFilters.forEach(function (el) {
          el.classList.remove("filter-active");
        });
        this.classList.add("filter-active");

        portfolioIsotope.arrange({
          filter: this.getAttribute("data-filter"),
        });
        portfolioIsotope.on("arrangeComplete", function () {
          AOS.refresh();
        });
      },
      true
    );
  }
}

document
  .querySelector("form#search")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    var product_name = document.getElementById("searchProduct").value;
    var csrf_token = document.getElementById("csrf_token_search").value;

    // Xóa các script hiện tại
    var scriptToRemove = document.querySelector(
      'script[src="/static/assets/vendor/isotope-layout/isotope.pkgd.min.js"]'
    );
    if (scriptToRemove) {
      scriptToRemove.remove();
    }

    // Sử dụng AJAX để gửi yêu cầu tìm kiếm
    $.ajax({
      url: "/portfolio/",
      type: "POST",
      data: { product_name: product_name, csrfmiddlewaretoken: csrf_token },
      success: function (response) {
        var products = response.products;
        console.log(products);
        var container = document.querySelector(".portfolio-container");
        // Xóa danh sách sản phẩm hiện tại
        container.innerHTML = "";
        // Thêm các sản phẩm tìm kiếm vào danh sách
        products.forEach(function (product) {
          container.innerHTML += `
                    <div class="col-lg-4 col-md-6 portfolio-item filter-${product.category.toLowerCase()}">
                        <img src="/media/${
                          product.image
                        }" class="img-fluid" alt="${product.product_name}" />
                        <div class="portfolio-info">
                            <h4>${product.product_name}</h4>    
                            <p>${product.category}</p>
                            <a href="/media/${
                              product.image
                            }" data-gallery="portfolioGallery" class="portfolio-lightbox preview-link" title="${
            product.product_name
          }"><i class="bx bx-plus"></i></a>
                            <a href="/${
                              product.id
                            }/detail" class="details-link" title="More Details"><i class="bx bx-link"></i></a>
                        </div>
                    </div>
                `;
        });
        filterProduct();
      },
      error: function (error) {
        console.error(error);
      },
    });
  });
