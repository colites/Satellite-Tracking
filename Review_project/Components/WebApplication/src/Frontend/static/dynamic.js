// ================================
// Input Page Dynamic UI Manipulation Functions
// ================================


/**
 * Changes the HTML to a search bar for product reviews.
 */
function htmlSearchProduct(){
	const newform = document.querySelector("#input_container");
	newform.innerHTML = `
        <div class="form-container">
            <h2>Search for a Product</h2>
            <label for="searchForProduct">Product Name:</label>
            <input type="text" id="searchForProduct" placeholder="Enter product name">
            <button type="button" onclick="searchProduct()">Search</button>
        </div>

        <button type="button" onclick="back()">Back</button>
    `;
}


/**
 * Changes the HTML to a product review form to be filled out.
 */
function htmlReviewProduct(){
	const newform = document.querySelector("#input_container");
	newform.innerHTML = `
        <div class="form-container">
            <h2>Post a Review</h2>
            <label for="reviewProduct">Product Name:</label>
            <input type="text" id="reviewProduct" name="reviewProduct" placeholder="Enter product name for review">

            <label for="productReview">Your Review:</label>
            <textarea id="productReview" name="productReview" rows="4" placeholder="Type your review here"></textarea>
            <button type="button" onclick="submitReview()">Submit Review</button>

            <div class="stars">
                <input type="radio" id="5-stars" name="rating" value="5" />
                <label for="5-stars" class="star">&#9733;</label>
                <input type="radio" id="4-stars" name="rating" value="4" />
                <label for="4-stars" class="star">&#9733;</label>
                <input type="radio" id="3-stars" name="rating" value="3" />
                <label for="3-stars" class="star">&#9733;</label>
                <input type="radio" id="2-stars" name="rating" value="2" />
                <label for="2-stars" class="star">&#9733;</label>
                <input type="radio" id="1-star" name="rating" value="1" />
                <label for="1-star" class="star">&#9733;</label>
            </div>
        </div>
        <button type="button" onclick="back()">Back</button>

    `;
}


function back(){
    window.location.href = '/';
}


function submitReview(){
    const productName = document.getElementById("#reviewProduct").value;
  	const productReview = document.getElementById("#productReview").value;
    //const stars = document.getElementById(".stars").value;
    
    const data = {
        productName: productName,
        reviewText: productReview
        //stars: stars
    };

    const response = fetch(`/submit-review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const newform = document.querySelector("#input_container");
    if (!response.ok) {
        newform.innerHTML = `
            <h1> Review Not Successfully Posted </h1>
            <button type="button" onclick="back()">Back</button>
        `
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
    }
    else {
        newform.innerHTML = `
            <h1> Review Successfully Posted </h1>
            <button type="button" onclick="back()">Back</button>
        `
    }
}       


function searchProduct(){

    const screen = document.querySelector("#input_container");
    const productName = document.getElementById("searchForProduct").value;

    fetch(`http://127.0.0.1:5001/query-data-frontend?productName=${productName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
			if (data === null) {
				throw new Error("data is null")
			}
            else {
                const rows = data.map(item => [
                    item.date,
                    item.product_name,
                    item.review_text,
                    item.stars,
                ]);

                screen.innerHTML = `
                    <table>
                        <tr>
                            <th>Date</th>
                            <th>Product Name</th>
                            <th>Review</th>
                            <th>Stars</th>
                        </tr>

                        ${rows.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('')}
                        
                    </table>
                    <button type="button" onclick="back()">Back</button>
                `
            }
        });
}