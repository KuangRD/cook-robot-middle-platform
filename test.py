import base64

if __name__ == "__main__":
    with open("./static/dish_img/test.png", mode="rb") as f:
        img = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf8")
        print(img)


