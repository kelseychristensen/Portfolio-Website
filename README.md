<h1 align="center">Portfolio Website</h1>

<p align="center">
This is a portfolio website for my web development projects. </a></p>



## Links

- [Repo](https://github.com/kelseychristensen/portfolio-website "portfolio-website")

## Screenshots

![Home](/static/snip1.PNG "Home")
![Portfolio](/static/snip2.PNG "Portfolio")
![Contact](/static/snip 3.PNG "Contact")
![Add New](/static/snip4.PNG "Add New")


### Built with

- HTML
- CSS
- Python
- Flask
- Bootstrap
- WTForms 
- Jinja

### What went into this project

I first worked on the UI in HTML and CSS before setting up a Flask server to serve all the files. I used Jinja templating to include the same header and footer on each page, and set up an SQL database to hold all my portfolio items. To add new items, I have given myself an easy WTForm interface so I don't have to code a new page. 

### Continued development

I definitely think the UI could be more sophisticated and interesting. I hope someday to really nail that aspect. 
```html
@app.route("/edit-item/<int:item_id>", methods=["GET", "POST"])
@admin_only
def new_item(item_id):
    item = Item.query.get(item_id)
    edit_form = CreateItemForm(
        title=item.title,
        img_url=item.img_url,
        description=item.description,
        github=item.github,
        dribbble=item.dribbble)

    if edit_form.validate_on_submit():
        item.title = edit_form.title.data
        item.img_url = edit_form.img_url.data
        item.description = edit_form.description.data
        item.github = edit_form.github.data
        item.dribbble = edit_form.dribbble.data
        db.session.commit()
        return redirect(url_for("show_item", item_id=item.id))
    return render_template("new_item.html", form=edit_form, is_edit=True, current_user=current_user)

```
```css
.bg-image {
    
/* RESPONSIVENESS */
@media (max-width: 1028px) {
    main {
        margin: 0
    }

    .welcome {
        padding: 0 20%;
    }

    .box {
        padding: 0;
    }

    img {
        width: 100%;
    }

    .box {
        position: static;
        margin: 0;
        width: 100%;
        background-color: rgb(180, 159, 148, 0);
    }

    .col-lg-6 {
        text-align: center;
    }

.image-container {
    margin: 0;
}

}



}
```
## Author

Kelsey Christensen

- [Profile](https://github.com/kelseychristensen "Kelsey Christensen")
- [Email](mailto:kelsey.c.christensen@gmail.com?subject=Hi "Hi!")
- [Dribble](https://dribbble.com/kelseychristensen "Hi!")
- [Website](http://kelseychristensen.com/ "Welcome")
