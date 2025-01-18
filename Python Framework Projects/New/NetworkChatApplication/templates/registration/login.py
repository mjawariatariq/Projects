<!-- login.html -->

{% extends 'base.html' %}

{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">

{% block title %}Login{% endblock %}

{% block content %}
  <div class="container">
    <!-- Log In ka alert message dikhana -->
    <h5 class="alert alert-info">Log In</h5>
    
    <!-- Form ko post method ke saath render kar rahe hain -->
    <form method="post">
      <!-- CSRF token ko include kar rahe hain for security -->
      {% csrf_token %}
      
      <!-- Form fields ko paragraph tags mein render kar rahe hain -->
      {{ form.as_p }}
      
      <!-- Submit button ko display kar rahe hain -->
      <button type="submit" class="btn btn-primary btn-lg btn-block">Log In</button>
    </form>
  </div>  
{% endblock %}

<script src="{% static 'chat.js' %}"></script>
