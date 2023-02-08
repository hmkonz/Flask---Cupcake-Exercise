const BASE_URL = "http://localhost:5000/api";

/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class= "delete-cupcake" data-id="{{cupcake.id}}">X</button>
            </li>
            <img class="cupcake-img" src="${cupcake.image}" alt="No image provided">
        </div>
    `;
}

/** put initial cupcakes on page. */

async function showInitialCupcakes() {
  const response = await axios.get("http://localhost:5000/api/cupcakes");
  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcake-list").append(newCupcake);
  }
}

// handle form for adding new cupcakes

$("#new-cupcake-form").on("submit", async function (event) {
  event.preventDefault();

  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(
    "http://localhost:5000/api/cupcakes",
    { flavor, size, rating, image }
  );

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcake-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});

// handle clicking delete: delete cupcake

$("#cupcake-list").on("click", ".delete-cupcake", async function (event) {
  event.preventDefault();
  let $cupcake = $(event.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`http://localhost:5000/api/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

// $(".delete-cupcake").click(deleteCupcake);

// async function deleteCupcake() {
//   const id = $(this).data("id");
//   await axios.delete(`http://localhost:5000/api/cupcakes/${id}`);
//   $(this).parent.remove();
// }

$(showInitialCupcakes);
