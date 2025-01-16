<!-- login.html -->

{% extends 'base.html' %}

{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">

{% block title %}Login{% endblock %}

{% block content %}
  <div class="container">
    <h5 class="alert alert-info">Log In</h5>
    <div class="btn btn-light d-flex justify-content-between" style="padding: 34px 30%;">
      <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary btn-lg btn-block">Log In</button>
      </form>
    </div>
  </div>  
{% endblock %}

{
