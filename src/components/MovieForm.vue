<template>
  <div>
    <div class="page-header1">
       <h1>Add A New Movie</h1>
  </div>
   
    <form id="MovieForm" @submit.prevent="saveMovie">
      <div v-if="success" class="alert alert-success">
        Movie successfully added
      </div>
      <div v-if="errors.length" class="alert alert-danger">
        <ul>
          <li v-for="error in errors">{{ error }}</li>
        </ul>
      </div>
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Movie Description</label>
        <textarea name="description" class="form-control"></textarea>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Photo Upload</label>
        <input type="file" name="poster" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
let success = ref(false);
let csrf_token = ref("");
let errors = ref([]);
let errorDisplayStatus = ref({});

function getCsrfToken() {
fetch('/api/v1/csrf-token')
  .then((response) => response.json())
  .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
  })
}

onMounted(() => {
  getCsrfToken();
});

function validateForm() {
  errors.value = [];
  errorDisplayStatus.value = {};

  let titleInput = document.getElementsByName("title")[0];
  let descriptionInput = document.getElementsByName("description")[0];
  let fileInput = document.getElementsByName("poster")[0];

  if (!titleInput.value) errors.value.push("Title is required");
  if (!descriptionInput.value) errors.value.push("Description is required");
  
  if (!fileInput.files.length) {
    errors.value.push("File is required");
  } else {
    let allowedExtensions = ["image/jpeg", "image/png"];
    if (!allowedExtensions.includes(fileInput.files[0].type)) {
      errors.value.push("Accepted file format: jpg, jpeg, png");
    }
  }

  return errors.value.length === 0;
}

function saveMovie() {
  let MovieForm = document.getElementById('MovieForm');
  let form_data = new FormData(MovieForm);

  if (validateForm()) {
    fetch("/api/v1/movies", {
      method: 'POST',
      body: form_data,
      headers: {
        'X-CSRFToken': csrf_token.value 
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const contentType = response.headers.get("Content-Type");
      if (contentType && contentType.includes("application/json")) {
        return response.json(); 
      } else {
        return Promise.reject('Expected JSON response, but received something else');
      }
    })
    .then(data => {
      console.log('Success:', data);
      if (data.message) {
        success.value = true;
      } else {
        errors.value.push(data.errors);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      errors.value.push("An error occurred: " + error);
    });
  }
}
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Lato:400,700");
.page-header1 {
text-align: center;
padding-right: 56%;
margin-bottom: 20px;
}
* { 
  -moz-box-sizing: border-box; 
  -webkit-box-sizing: border-box; 
  box-sizing: border-box;
  
}
form{
  margin: 55px;
}
label{
  display: block;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 10px;
}
input, textarea{
  max-width: 700px;
  width: 100%;
}
#poster{
  border: 1px solid black;
}
</style>