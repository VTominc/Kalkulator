#!/usr/bin/env python
import os
import jinja2

import webapp2

                                    # "jinja-basic-gae-project-master"
                                    # "jinja-...-master" + "/" + "templates"
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class OmeniHandler(BaseHandler):
    def get(self):
        return self.render_template("omeni.html") # , params=params)

class RezultatHandler(BaseHandler):
    def post(self):
        vnos = self.request.get("vnos")
        return self.write("Vnesel si: '{}'".format(vnos))

class BMIHandler(BaseHandler):
    def get(self):
        return self.render_template("bmicak.html")

    def post(self):
        visina = float(self.request.get("visina"))
        teza = float(self.request.get("teza"))
        bmi = teza / visina**2
        return self.write("BMI: {}".format(bmi))

class KalkulatorHandler(BaseHandler):
    def get(self):
        return self.render_template(("kalkulator.html"))

    def post(self):
        first_number = float(self.request.get("firstnumber"))
        second_number = float(self.request.get("secondnumber"))
        operation = self.request.get("operation")



        if operation == "+":
            result = first_number + second_number
        elif operation == "-":
            result = first_number - second_number
        elif operation == "*":
            result = first_number * second_number
        elif operation == "/":
            result = first_number / second_number
        elif operation == "**":
            result = first_number ** second_number
        elif operation == "%":
            result = first_number % second_number

        return self.write("Rezultat je {}".format(result))


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/omeni', OmeniHandler),       # Podstran!
    webapp2.Route('/rezultat', RezultatHandler), # Pazi na vejice!
    webapp2.Route('/bmi', BMIHandler),
    webapp2.Route('/kalkulator', KalkulatorHandler)
], debug=True)
