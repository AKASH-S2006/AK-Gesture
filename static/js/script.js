// Smooth scrolling for navigation

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
        .scrollIntoView({

            behavior:"smooth"

        });

    });

});
// ===============================
// Feature Switching
// ===============================

const cards = document.querySelectorAll(".card");

cards.forEach(card => {

    card.addEventListener("click", () => {

        const mode = card.dataset.mode;

        if (!mode) return;

        fetch("/set_mode",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                mode:mode

            })

        })

        .then(res=>res.json())

        .then(data=>{

            console.log(data);

            cards.forEach(c=>{

                c.classList.remove("active-card");

            });

            card.classList.add("active-card");

        });

    });

});
