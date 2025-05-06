{% with class_title="APCSP: More Binary" %}
{% include 'components/title_slide.md' %}
{% endwith %}

{% include2 './warmup.md' %}


{% include2 '../Day0/recap.md' %}


# Today: Images -> Binary

## Vocab review:
- Analog: Information in the real world
- Digital: Information converted for storage on a computer
- Abstraction: Taking something complex and making a simpler version
- Sampling: Collecting little pieces of information
- Loss: Information that you lose from sampling

## One more - Who is this?
![](../../images/lofi_girl.jpg)

## Fidelity
How closely does the digital information match the analog information?

- Low fideltiy ("lofi") - the digital version does not match the analog version very well
- High fidelity ("hifi") - the digital version does match the analog version well

## Images: Levels of abstraction
1. Divide an image into pixels
2. Convert each pixel into a single color
3. Map each color to the closest available color
4. Convert the color to binary

## Practice - Code.org Pixelation Tool
- Start with B&W

## Each pixel is actually 3 lights
![Primary colors](../../images/primary_colors.jpg)



## Practice - with colors
- Can you recreate this, using 3 bits per pixel?
![](../../images/9colors.png)


{% include2 './recap.md' %}

