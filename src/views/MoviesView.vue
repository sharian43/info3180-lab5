<template>
    <div class="page-header">
      <h2>Movies</h2>
  </div>
  
      <div class="movies-container">
        <div class="row">
          <div class="col-sm-6 mb-3" v-for="movie in movies" :key="movie.id">
            <div class="card h-100">
              <div class="row no-gutters h-100">
                <div class="col-md-4 h-100">
                  <img :src="movie.poster" class="card-img h-100" alt="Movie Poster">
                </div>
                <div class="col-md-8">
                  <div class="card-body">
                    <h5 class="card-title">{{ movie.title }}</h5>
                    <p class="card-text">{{ movie.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <style scoped>
    .page-header {
      text-align: center;
      margin-bottom: 20px;
  }
    .movies-container {
      max-width: 1000px;
      margin: 0 auto;
    }
    
    .card {
      transition: 0.3s;
      border: 2.5px solid #f2f7fd;
      border-radius: 5px;
      height: 100%;
    }
    
    .card:hover {
      box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
    }
    
    .card-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    
    .card-body {
      height: 100%;
      padding-left: 2px;
    }
    .col-md-8{
      padding-left: 2px;
    }
    
  </style>
     
  <script setup>
      import { ref, onMounted } from "vue";
      let movies = ref([]);
      async function fetchMovies(){
          try {
              const response = await fetch('/api/v1/movies');
              const data = await response.json()
              movies.value = data.movies;
          } 
          catch (error) {
              console.error(error);
          }
      }
      onMounted(fetchMovies);
  </script>