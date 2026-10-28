# Near-duplicate pairs to read (Stage 3 step 3)

317 flagged pairs; 20 shown. Verdicts by Heshmat, 29 Oct 2026 (full text checked): 7 real duplicates, 13 same passage with a different question, 0 unrelated.

## Pair 1: near_0.97 (train, TAUR-Lab/MuSR/object_placements) vs (test, TAUR-Lab/MuSR/object_placements)

**A** `c44d5b5b6b20`

```
Story:
Olivia, drained after another demanding day at the office, rushed home for the evening, unaware that she had left behind her mobile phone filled with photos that were priceless to her. Her workspace, scattered with papers, was also home to her half-drunk cup of coffee. Ben, the ever-curious co-worker, could never resist an unmanned desk. As the day dwindled, his habit of sneaking glances at his colleagues' desks was well-known, making him aware, as everybody else was, about the location of Olivia's missing phone and the abandoned cup of coffee. Emily, the dedicated night janitor, had the solemn task of tidying up the workspaces long after everyone else had gone home, including safely 
[...]
via tried not to let her imagination get the best of her. For now, all she could do was to watch in silence as Emily went about her duties. And while the echo of the clinking ceramics was the only sound that managed to pierce the eerie quiet of the deserted office, it was enough to signal another successful night for Emily. The office space, now as pristine as a picture, and the lingering scent of cleaning products served as a quiet testament to her dedication and professionalism. A fitting end to another day in the office, with a conclusion that was silently eloquent in its simplicity, doubtlessly waiting for the dawn of a new day.

Question: Which location is the most likely place Ben would look to find the cup of coffee given the story?

Choices: Lost and Found box,desk,drawer,kitchen


```

**B** `c8841e71b30c`

```
Story:
Olivia, drained after another demanding day at the office, rushed home for the evening, unaware that she had left behind her mobile phone filled with photos that were priceless to her. Her workspace, scattered with papers, was also home to her half-drunk cup of coffee. Ben, the ever-curious co-worker, could never resist an unmanned desk. As the day dwindled, his habit of sneaking glances at his colleagues' desks was well-known, making him aware, as everybody else was, about the location of Olivia's missing phone and the abandoned cup of coffee. Emily, the dedicated night janitor, had the solemn task of tidying up the workspaces long after everyone else had gone home, including safely 
[...]
ivia tried not to let her imagination get the best of her. For now, all she could do was to watch in silence as Emily went about her duties. And while the echo of the clinking ceramics was the only sound that managed to pierce the eerie quiet of the deserted office, it was enough to signal another successful night for Emily. The office space, now as pristine as a picture, and the lingering scent of cleaning products served as a quiet testament to her dedication and professionalism. A fitting end to another day in the office, with a conclusion that was silently eloquent in its simplicity, doubtlessly waiting for the dawn of a new day.

Question: Which location is the most likely place Ben would look to find the mobile phone given the story?

Choices: Lost and Found box,desk,drawer,kitchen


```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 2: near_1.00 (train, TAUR-Lab/MuSR/object_placements) vs (calibration, TAUR-Lab/MuSR/object_placements)

**A** `e5e479039ddc`

```
Story:
Frank, an eager student, had enrolled in Marcy's yoga class with the hope of improving his flexibility. A keen observer, he found learning by watching Marcy enact the postures much more instructive than attempting them on his own. Marcy was a meticulous instructor, ensuring her students understood the positions correctly as she demonstrated on her yoga mat. She always knew exactly where her yoga mat was, in the storage cabin, ready to be rolled out on the studio floor for her demonstrations. Nearby, a water bottle was always kept in the yoga hall, a reminder to stay hydrated during the sessions. Lisa, the diligent janitor of the setup, was responsible for maintaining the studio's clea
[...]
ing, based on careful demonstrations rather than verbal description alone, had once again proven effective.

As the last participant left the training space, the echo of the concluded yoga class still lingered. Frank, now alone, made way towards the storage cabin, fulfilling his role as an unexpected helper. Lisa returned to an already clean studio, her service beautifully complemented by Frank’s unseen initiative.

And so, another day came to a close at the yoga studio. With Marcy’s instructive guidance, Frank’s newfound enthusiasm, and Lisa's dedicated efforts, a harmonious balance was maintained, marking the end of a productive day.

Question: Which location is the most likely place Lisa would look to find the water bottle given the story?

Choices: locker room,storage cabin,yoga hall


```

**B** `839aac88e911`

```
Story:
Frank, an eager student, had enrolled in Marcy's yoga class with the hope of improving his flexibility. A keen observer, he found learning by watching Marcy enact the postures much more instructive than attempting them on his own. Marcy was a meticulous instructor, ensuring her students understood the positions correctly as she demonstrated on her yoga mat. She always knew exactly where her yoga mat was, in the storage cabin, ready to be rolled out on the studio floor for her demonstrations. Nearby, a water bottle was always kept in the yoga hall, a reminder to stay hydrated during the sessions. Lisa, the diligent janitor of the setup, was responsible for maintaining the studio's clea
[...]
ng, based on careful demonstrations rather than verbal description alone, had once again proven effective.

As the last participant left the training space, the echo of the concluded yoga class still lingered. Frank, now alone, made way towards the storage cabin, fulfilling his role as an unexpected helper. Lisa returned to an already clean studio, her service beautifully complemented by Frank’s unseen initiative.

And so, another day came to a close at the yoga studio. With Marcy’s instructive guidance, Frank’s newfound enthusiasm, and Lisa's dedicated efforts, a harmonious balance was maintained, marking the end of a productive day.

Question: Which location is the most likely place Frank would look to find the water bottle given the story?

Choices: locker room,storage cabin,yoga hall


```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 3: near_0.99 (train, TAUR-Lab/MuSR/object_placements) vs (test, TAUR-Lab/MuSR/object_placements)

**A** `e5e479039ddc`

```
Story:
Frank, an eager student, had enrolled in Marcy's yoga class with the hope of improving his flexibility. A keen observer, he found learning by watching Marcy enact the postures much more instructive than attempting them on his own. Marcy was a meticulous instructor, ensuring her students understood the positions correctly as she demonstrated on her yoga mat. She always knew exactly where her yoga mat was, in the storage cabin, ready to be rolled out on the studio floor for her demonstrations. Nearby, a water bottle was always kept in the yoga hall, a reminder to stay hydrated during the sessions. Lisa, the diligent janitor of the setup, was responsible for maintaining the studio's clea
[...]
ing, based on careful demonstrations rather than verbal description alone, had once again proven effective.

As the last participant left the training space, the echo of the concluded yoga class still lingered. Frank, now alone, made way towards the storage cabin, fulfilling his role as an unexpected helper. Lisa returned to an already clean studio, her service beautifully complemented by Frank’s unseen initiative.

And so, another day came to a close at the yoga studio. With Marcy’s instructive guidance, Frank’s newfound enthusiasm, and Lisa's dedicated efforts, a harmonious balance was maintained, marking the end of a productive day.

Question: Which location is the most likely place Lisa would look to find the water bottle given the story?

Choices: locker room,storage cabin,yoga hall


```

**B** `6f06c7e15617`

```
Story:
Frank, an eager student, had enrolled in Marcy's yoga class with the hope of improving his flexibility. A keen observer, he found learning by watching Marcy enact the postures much more instructive than attempting them on his own. Marcy was a meticulous instructor, ensuring her students understood the positions correctly as she demonstrated on her yoga mat. She always knew exactly where her yoga mat was, in the storage cabin, ready to be rolled out on the studio floor for her demonstrations. Nearby, a water bottle was always kept in the yoga hall, a reminder to stay hydrated during the sessions. Lisa, the diligent janitor of the setup, was responsible for maintaining the studio's clea
[...]
aching, based on careful demonstrations rather than verbal description alone, had once again proven effective.

As the last participant left the training space, the echo of the concluded yoga class still lingered. Frank, now alone, made way towards the storage cabin, fulfilling his role as an unexpected helper. Lisa returned to an already clean studio, her service beautifully complemented by Frank’s unseen initiative.

And so, another day came to a close at the yoga studio. With Marcy’s instructive guidance, Frank’s newfound enthusiasm, and Lisa's dedicated efforts, a harmonious balance was maintained, marking the end of a productive day.

Question: Which location is the most likely place Marcy would look to find the yoga mat given the story?

Choices: locker room,storage cabin,yoga hall


```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 4: near_0.97 (train, rungalileo/ragbench/cuad) vs (test, rungalileo/ragbench/cuad)

**A** `f8b59ec8d775`

```
Use the following pieces of context to answer the question.

Exhibit 10.8

eGAIN COMMUNICATIONS CORPORATION

HOSTING AGREEMENT

1. Hosting Agreement. This Agreement (including its Exhibit A and all other documents referenced herein) is entered into by eGain Communications Corporation ("eGain") and Eliance Corporation ("Customer") for the purpose of providing Customer with Web-based access to eGain's software specified in Exhibit A, including any updates, upgrades or revisions provided under this Agreement ("Software"), and certain other services relating to the processing of and response to online inquiries and messages ("Online Messages") received by Customer from its customers and other us
[...]
and assets of a party. This Agreement will bind and inure to the benefit of the parties and their successors and permitted assigns.

Each party agrees to the terms and conditions contained in this Agreement.

Customer: Eliance Corporation

Name:/s/                                 Title:                              ___________________________               _________

Signature:______________________         Date:__________

eGain Communications Corporation:

Name:/s/                                 Title:                              ___________________________               _________

Signature:______________________         Date:__________

Question: Is there a minimum order size or minimum amount or units per-time period that one party must buy from the counterparty under the contract?

```

**B** `5fa0575102fa`

```
Use the following pieces of context to answer the question.

Exhibit 10.8

eGAIN COMMUNICATIONS CORPORATION

HOSTING AGREEMENT

1. Hosting Agreement. This Agreement (including its Exhibit A and all other documents referenced herein) is entered into by eGain Communications Corporation ("eGain") and Eliance Corporation ("Customer") for the purpose of providing Customer with Web-based access to eGain's software specified in Exhibit A, including any updates, upgrades or revisions provided under this Agreement ("Software"), and certain other services relating to the processing of and response to online inquiries and messages ("Online Messages") received by Customer from its customers and other us
[...]
nd assets of a party. This Agreement will bind and inure to the benefit of the parties and their successors and permitted assigns.

Each party agrees to the terms and conditions contained in this Agreement.

Customer: Eliance Corporation

Name:/s/                                 Title:                              ___________________________               _________

Signature:______________________         Date:__________

eGain Communications Corporation:

Name:/s/                                 Title:                              ___________________________               _________

Signature:______________________         Date:__________

Question: Does a party have the right to  audit the books, records, or physical locations of the counterparty to ensure compliance with the contract?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 5: near_1.00 (train, rungalileo/ragbench/cuad) vs (calibration, rungalileo/ragbench/cuad)

**A** `3def6bedc711`

```
Use the following pieces of context to answer the question.

EXHIBIT 10.3

   [ABOUT LOGO]

CO-BRANDING AGREEMENT

This Agreement (the "Agreement"), dated this 19th day of January, 2001 (the "Effective Date"), is by and between About.com, Inc. ("About"), a Delaware corporation, located at 1440 Broadway, 19th Floor, New York, NY 10018 and ebix.com, Inc. ("ebix"), a Delaware corporation, located at 1900 E.Golf Road, Schaumberg, IL 60173

W I T N E S S E T H:

WHEREAS, About owns and operates an Internet service known as About.com, currently located at the URL HTTP://WWW.ABOUT.COM, at which users may access a variety of content channels and a network of highly-targeted, topic-specific Web sites
[...]
tle:       ------------------------------           ------------------------------

Signature:                               Signature:           --------------------------               --------------------------

Date:                                    Date:      -------------------------------          -------------------------------

** Confidential treatment has been requested for portions of this document.    The redacted material has been filed with the commission pursuant to an    application for confidential treatment.

                                       11

Source: EBIX INC, 10-Q, 5/15/2001

Question: Is there a restriction on a party’s soliciting or hiring employees and/or contractors from the  counterparty, whether during the contract or after the contract ends (or both)?

```

**B** `205c6576ab52`

```
Use the following pieces of context to answer the question.

EXHIBIT 10.3

   [ABOUT LOGO]

CO-BRANDING AGREEMENT

This Agreement (the "Agreement"), dated this 19th day of January, 2001 (the "Effective Date"), is by and between About.com, Inc. ("About"), a Delaware corporation, located at 1440 Broadway, 19th Floor, New York, NY 10018 and ebix.com, Inc. ("ebix"), a Delaware corporation, located at 1900 E.Golf Road, Schaumberg, IL 60173

W I T N E S S E T H:

WHEREAS, About owns and operates an Internet service known as About.com, currently located at the URL HTTP://WWW.ABOUT.COM, at which users may access a variety of content channels and a network of highly-targeted, topic-specific Web sites
[...]
------

Title:                                   Title:       ------------------------------           ------------------------------

Signature:                               Signature:           --------------------------               --------------------------

Date:                                    Date:      -------------------------------          -------------------------------

** Confidential treatment has been requested for portions of this document.    The redacted material has been filed with the commission pursuant to an    application for confidential treatment.

                                       11

Source: EBIX INC, 10-Q, 5/15/2001

Question: Does the contract contain a license grant to a licensee (incl. sublicensor) and the affiliates of such licensee/sublicensor?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 6: near_0.99 (train, rungalileo/ragbench/cuad) vs (threshold, rungalileo/ragbench/cuad)

**A** `20fa78f1df6a`

```
Use the following pieces of context to answer the question.

CONFIDENTIAL PORTIONS OMITTED

                                                                   EXHIBIT 10.16

                       [LOGO OF TEAM SABCO APPEARS HERE]

                             SPONSORSHIP AGREEMENT

THIS SPONSORSHIP AGREEMENT (hereinafter the "Agreement) is made and entered into this 19th day of December 1997, by and between SABCO RACING, INC., a North Carolina corporation with a place of business in Iredell County, North Carolina (hereinafter Sabco), and Prolong Super Lubricants, Anaheim, Calif. (Hereinafter to be referred to as "Prolong");

                                  WITNESSETH:

     WHEREAS, Sabco
[...]
en.





                               SABCO RACING, INC. ATTEST:                                                                 BY /s/ Armando Fitz                                   -------------------------------- /s/ Jerry Grant                Armando Fitz - Vice President Business Operations - --------------------------    Jerry Grant - Secretary

                               PROLONG SUPER LUBRICANTS ATTEST:

                               BY /s/ Elton Alderman /s/ ILLEGIBLE                     --------------------------------- - --------------------------              Elton Alderman - President                  Secretary

Question: Is there a restriction on the ability of a party to compete with the counterparty or operate in a certain geography or business or technology sector? 

```

**B** `29596b9814d0`

```
Use the following pieces of context to answer the question.

CONFIDENTIAL PORTIONS OMITTED

                                                                   EXHIBIT 10.16

                       [LOGO OF TEAM SABCO APPEARS HERE]

                             SPONSORSHIP AGREEMENT

THIS SPONSORSHIP AGREEMENT (hereinafter the "Agreement) is made and entered into this 19th day of December 1997, by and between SABCO RACING, INC., a North Carolina corporation with a place of business in Iredell County, North Carolina (hereinafter Sabco), and Prolong Super Lubricants, Anaheim, Calif. (Hereinafter to be referred to as "Prolong");

                                  WITNESSETH:

     WHEREAS, Sabco
[...]
 officers as of the day and year first above  written.





                               SABCO RACING, INC. ATTEST:                                                                 BY /s/ Armando Fitz                                   -------------------------------- /s/ Jerry Grant                Armando Fitz - Vice President Business Operations - --------------------------    Jerry Grant - Secretary

                               PROLONG SUPER LUBRICANTS ATTEST:

                               BY /s/ Elton Alderman /s/ ILLEGIBLE                     --------------------------------- - --------------------------              Elton Alderman - President                  Secretary

Question: Is there a clause granting one party an “enterprise,” “all you can eat” or unlimited usage license?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 7: near_1.00 (train, openhermes/teknium) vs (calibration, openhermes/teknium)

**A** `e3c5e7acc0c9`

```
BEGININPUT
BEGINCONTEXT

ENDCONTEXT
---

Welcome to TechSavvy's annual review of the latest gadgets that have taken the world by storm! This year has been an exciting one for tech enthusiasts, with numerous innovative devices hitting the market. In this article, we'll be taking a look at some of the standout products that have captured our attention in 2021.

### 1. Zephyr X10 Drone

The Zephyr X10 is a state-of-the-art drone designed by FlyTech Industries. Released on March 15th, it boasts an impressive flight time of up to 40 minutes and can reach speeds of up to 50 mph. The drone also features a high-quality camera capable of capturing stunning 4K video footage. With its advanced obstacle
[...]
or $3,499.

### 5. SoundScape Pro Wireless Earbuds

Rounding out our list are the SoundScape Pro wireless earbuds by AudioRevolution. Launched on September 30th, these earbuds offer exceptional sound quality and noise-canceling capabilities, along with an impressive battery life of up to 10 hours. Their sleek design and comfortable fit make them perfect for everyday use or intense workouts. The SoundScape Pro earbuds retail for $199.

As we wrap up another year filled with exciting technological advancements, we can't wait to see what new gadgets will be released in the coming months. Stay tuned to TechSavvy for all the latest updates on your favorite tech products!
ENDINPUT
BEGININSTRUCTION
make a markdown table summarizing the top 5 most popular products, their prices, and release dates

```

**B** `b386de8d7ee0`

```
BEGININPUT
BEGINCONTEXT

ENDCONTEXT
---

Welcome to TechSavvy's annual review of the latest gadgets that have taken the world by storm! This year has been an exciting one for tech enthusiasts, with numerous innovative devices hitting the market. In this article, we'll be taking a look at some of the standout products that have captured our attention in 2021.

### 1. Zephyr X10 Drone

The Zephyr X10 is a state-of-the-art drone designed by FlyTech Industries. Released on March 15th, it boasts an impressive flight time of up to 40 minutes and can reach speeds of up to 50 mph. The drone also features a high-quality camera capable of capturing stunning 4K video footage. With its advanced obstacle
[...]
5. SoundScape Pro Wireless Earbuds

Rounding out our list are the SoundScape Pro wireless earbuds by AudioRevolution. Launched on September 30th, these earbuds offer exceptional sound quality and noise-canceling capabilities, along with an impressive battery life of up to 10 hours. Their sleek design and comfortable fit make them perfect for everyday use or intense workouts. The SoundScape Pro earbuds retail for $199.

As we wrap up another year filled with exciting technological advancements, we can't wait to see what new gadgets will be released in the coming months. Stay tuned to TechSavvy for all the latest updates on your favorite tech products!
ENDINPUT
BEGININSTRUCTION
make a markdown table summarizing the top 5 most popular products, their prices, and release dates
ENDINSTRUCTION


```

Verdict: real duplicate (same question)

## Pair 8: near_1.00 (train, openhermes/teknium) vs (test, openhermes/teknium)

**A** `48d05f6aae78`

```
BEGININPUT
BEGINCONTEXT
date: August 29, 2009
ENDCONTEXT
Liracorp, a relatively unknown tech startup based in Zoristan, has recently announced their latest invention: the "Agrivator 3000." This cutting-edge device is designed to revolutionize the agricultural industry by optimizing crop growth and minimizing resource waste.

The Agrivator 3000 works by using advanced sensor technology to monitor various factors that influence plant growth, such as soil moisture levels, temperature, and nutrient content. The device then uses this data to create an ideal environment for each specific crop, adjusting irrigation systems, fertilizers, and other resources accordingly.

One of the key features of t
[...]
 farmers.

Liracorp CEO, Elara Tannin, stated in a recent press conference that the Agrivator 3000 has already undergone extensive testing on several farms in the Zoristan region. According to Tannin, early results have been overwhelmingly positive, with participating farmers reporting significant improvements in crop yields and reductions in water usage.

While the Agrivator 3000 is still in its early stages of development, Liracorp hopes to begin mass production within the next two years. If successful, this innovative device could potentially transform the way we approach agriculture, ushering in a new era of efficiency and sustainability.
ENDINPUT
BEGININSTRUCTION
Explain how Liracorp's new invention could potentially impact the field of agriculture.

What date is your response from?


```

**B** `354d1b05427f`

```
BEGININPUT
BEGINCONTEXT
date: August 29, 2009
ENDCONTEXT
Liracorp, a relatively unknown tech startup based in Zoristan, has recently announced their latest invention: the "Agrivator 3000." This cutting-edge device is designed to revolutionize the agricultural industry by optimizing crop growth and minimizing resource waste.

The Agrivator 3000 works by using advanced sensor technology to monitor various factors that influence plant growth, such as soil moisture levels, temperature, and nutrient content. The device then uses this data to create an ideal environment for each specific crop, adjusting irrigation systems, fertilizers, and other resources accordingly.

One of the key features of t
[...]
orp CEO, Elara Tannin, stated in a recent press conference that the Agrivator 3000 has already undergone extensive testing on several farms in the Zoristan region. According to Tannin, early results have been overwhelmingly positive, with participating farmers reporting significant improvements in crop yields and reductions in water usage.

While the Agrivator 3000 is still in its early stages of development, Liracorp hopes to begin mass production within the next two years. If successful, this innovative device could potentially transform the way we approach agriculture, ushering in a new era of efficiency and sustainability.
ENDINPUT
BEGININSTRUCTION
Explain how Liracorp's new invention could potentially impact the field of agriculture.

What date is your response from?

ENDINSTRUCTION


```

Verdict: real duplicate (same question)

## Pair 9: near_0.99 (train, openhermes/teknium) vs (test, openhermes/teknium)

**A** `4aa5a10a013a`

```
BEGININPUT
BEGINCONTEXT
author: John Doe
title: A Brief History of Timekeeping Devices
publication: Historical Insights Magazine
date: 2022-02-15
url: www.historicalinsights.com/timekeeping-devices
ENDCONTEXT
The history of timekeeping devices dates back thousands of years. From ancient civilizations using sundials to track the movement of the sun, to the invention of mechanical clocks in medieval Europe, humans have always been fascinated by measuring time. In this article, we will explore some of the most significant developments in timekeeping technology throughout history, including the water clock, pendulum clock, and quartz watch.
ENDINPUT

BEGININPUT
BEGINCONTEXT
date: 2022-01-25
send
[...]
eef, Australia
coordinates: -18.2871, 147.6992
date: 2022-01-30
videographer: Sarah Johnson
transcript_title: Exploring the Great Barrier Reef
ENDCONTEXT
In this video, we take you on a journey through the breathtaking beauty of the Great Barrier Reef, one of the world's most famous natural wonders. Home to thousands of species of marine life, the reef stretches over 2,300 kilometers along the northeastern coast of Australia. As we dive beneath the surface, we encounter vibrant coral gardens, schools of colorful fish, and majestic sea turtles gliding gracefully through the water. Join us as we explore this incredible underwater paradise.
ENDINPUT

BEGININSTRUCTION
Explain the significance of the water clock and pendulum clock in the history of timekeeping devices.  Source?
ENDINSTRUCTION


```

**B** `02ee114ce978`

```
BEGININPUT
BEGINCONTEXT
author: John Doe
title: A Brief History of Timekeeping Devices
publication: Historical Insights Magazine
date: 2022-02-15
url: www.historicalinsights.com/timekeeping-devices
ENDCONTEXT
The history of timekeeping devices dates back thousands of years. From ancient civilizations using sundials to track the movement of the sun, to the invention of mechanical clocks in medieval Europe, humans have always been fascinated by measuring time. In this article, we will explore some of the most significant developments in timekeeping technology throughout history, including the water clock, pendulum clock, and quartz watch.
ENDINPUT

BEGININPUT
BEGINCONTEXT
date: 2022-01-25
send
[...]
 Great Barrier Reef, Australia
coordinates: -18.2871, 147.6992
date: 2022-01-30
videographer: Sarah Johnson
transcript_title: Exploring the Great Barrier Reef
ENDCONTEXT
In this video, we take you on a journey through the breathtaking beauty of the Great Barrier Reef, one of the world's most famous natural wonders. Home to thousands of species of marine life, the reef stretches over 2,300 kilometers along the northeastern coast of Australia. As we dive beneath the surface, we encounter vibrant coral gardens, schools of colorful fish, and majestic sea turtles gliding gracefully through the water. Join us as we explore this incredible underwater paradise.
ENDINPUT

BEGININSTRUCTION
Explain the significance of the water clock and pendulum clock in the history of timekeeping devices.  Source?

```

Verdict: real duplicate (same question)

## Pair 10: near_0.95 (train, rungalileo/ragbench/tatqa) vs (test, rungalileo/ragbench/tatqa)

**A** `da3453cce314`

```
Use the following pieces of context to answer the question.

Non-GAAP Results [["Reconciliation of Non-GAAP measure - operating expenses and operating income from continuing operations, excluding certain items (in thousands)", "Years Ended December 31,", ""], ["", "2019", "2018"], ["Gross profit from continuing operations, as reported", "$ 315,652", "$365,607"], ["Adjustments to gross profit:", "", ""], ["Stock-based compensation", "525", "742"], ["Facility expansion and relocation costs", "3,891", "1,328"], ["Acquisition-related costs", "8,290", "569"], ["Non-GAAP gross profit", "328,358", "368,246"], ["Non-GAAP gross margin", "41.6%", "51.2%"], ["Operating expenses from continuing operatio
[...]
dditional information should not be considered a substitute for results prepared in accordance with U.S. GAAP.


The non-GAAP results presented below exclude the impact of non-cash related charges, such as stock-based compensation and amortization of intangible assets. In addition, they exclude discontinued operations and other nonrecurring items such as acquisition-related costs and restructuring expenses, as they are not indicative of future performance. The tax effect of our non-GAAP adjustments represents the anticipated annual tax rate applied to each non-GAAP adjustment after consideration of their respective book and tax treatments and effect of adoption of the Tax Act.

Question: What was the change in the Gross profit from continuing operations, as reported between 2018 and 2019?

```

**B** `e1eef3f0c12c`

```
Use the following pieces of context to answer the question.

Non-GAAP Results [["Reconciliation of Non-GAAP measure - operating expenses and operating income from continuing operations, excluding certain items (in thousands)", "Years Ended December 31,", ""], ["", "2019", "2018"], ["Gross profit from continuing operations, as reported", "$ 315,652", "$365,607"], ["Adjustments to gross profit:", "", ""], ["Stock-based compensation", "525", "742"], ["Facility expansion and relocation costs", "3,891", "1,328"], ["Acquisition-related costs", "8,290", "569"], ["Non-GAAP gross profit", "328,358", "368,246"], ["Non-GAAP gross margin", "41.6%", "51.2%"], ["Operating expenses from continuing operatio
[...]
 from the perspective of management. The presentation of this additional information should not be considered a substitute for results prepared in accordance with U.S. GAAP.


The non-GAAP results presented below exclude the impact of non-cash related charges, such as stock-based compensation and amortization of intangible assets. In addition, they exclude discontinued operations and other nonrecurring items such as acquisition-related costs and restructuring expenses, as they are not indicative of future performance. The tax effect of our non-GAAP adjustments represents the anticipated annual tax rate applied to each non-GAAP adjustment after consideration of their respective book and tax treatments and effect of adoption of the Tax Act.

Question: What does the non-GAAP results exclude?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 11: near_0.95 (train, rungalileo/ragbench/emanual) vs (test, rungalileo/ragbench/emanual)

**A** `21173eb5e51e`

```
Use the following pieces of context to answer the question.

There Is a Problem with the Picture. When the TV has trouble with the picture, these steps may help resolve the problem.


Setting the screen to black and white. Settings General Accessibility Grayscale Try Now You can change the color of the TV screen to black and white to sharpen blurred edges caused by colors. Grayscale is on, some Accessibility menus are not available. This function may not be supported depending on the model or geographical area.


Testing the picture. Settings Support Self Diagnosis Start Picture Test Try Now Before you review the list of problems and solutions below, use Start Picture Test to determine if th
[...]
Settings Picture Picture Mode Settings Picture Expert Settings Brightness Settings Picture Expert Settings Sharpness Settings Picture Expert Settings Color See if Power Saving Mode has been enabled. Settings General Eco Solution Power Saving Mode Try resetting the picture. Settings Picture Expert Settings Reset Picture Change Picture Size Settings 16:9 Standard Settings Picture Picture Size Settings 16:9 Standard If you are using AV or analog equipment, disconnect the adapter from the Component (Blue) input port on the TV and connect it to the AV (Yellow) input port. The Component or AV input port may not be provided depending on the model or geographical area. Check whether Grayscale is set to Settings General Accessibility Grayscale 

Question: How do I fix blurring issues on TV screen?

```

**B** `12a245646024`

```
Use the following pieces of context to answer the question.

Testing the picture. Settings Support Self Diagnosis Start Picture Test Try Now Before you review the list of problems and solutions below, use Start Picture Test to determine if the problem is caused by the TV. Start Picture Test displays a high definition picture you can examine for flaws or faults. The problem Try this! Flickering and Dimming Component Connections/ Screen Color Screen Brightness Ghosting, Blurring, or Juddering If your TV is flickering or dimming sporadically, you may need to disable some of the energy efficiency features. Disable Ambient Light Detection Power Saving Mode , or Motion Lighting Settings General Ec
[...]
the adapter from the Component (Blue) input port on the TV and connect it to the AV (Yellow) input port. The Component or AV input port may not be provided depending on the model or geographical area. Check whether Grayscale is set to Settings General Accessibility Grayscale 


There Is a Problem with the Picture. When the TV has trouble with the picture, these steps may help resolve the problem.


Inverting the screen color. Settings General Accessibility Color Inversion Try Now You can invert the colors of the text and background displayed on the TV screen to make it easier to read them. Color Inversion is on, some Accessibility menus are not available. This function may not be supported depending on the model or geographical area.

Question: How do I fix the missing/wrong color issue ?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 12: near_0.95 (train, rungalileo/ragbench/emanual) vs (threshold, rungalileo/ragbench/emanual)

**A** `21173eb5e51e`

```
Use the following pieces of context to answer the question.

There Is a Problem with the Picture. When the TV has trouble with the picture, these steps may help resolve the problem.


Setting the screen to black and white. Settings General Accessibility Grayscale Try Now You can change the color of the TV screen to black and white to sharpen blurred edges caused by colors. Grayscale is on, some Accessibility menus are not available. This function may not be supported depending on the model or geographical area.


Testing the picture. Settings Support Self Diagnosis Start Picture Test Try Now Before you review the list of problems and solutions below, use Start Picture Test to determine if th
[...]
Settings Picture Picture Mode Settings Picture Expert Settings Brightness Settings Picture Expert Settings Sharpness Settings Picture Expert Settings Color See if Power Saving Mode has been enabled. Settings General Eco Solution Power Saving Mode Try resetting the picture. Settings Picture Expert Settings Reset Picture Change Picture Size Settings 16:9 Standard Settings Picture Picture Size Settings 16:9 Standard If you are using AV or analog equipment, disconnect the adapter from the Component (Blue) input port on the TV and connect it to the AV (Yellow) input port. The Component or AV input port may not be provided depending on the model or geographical area. Check whether Grayscale is set to Settings General Accessibility Grayscale 

Question: How do I fix blurring issues on TV screen?

```

**B** `b48348a8df4c`

```
Use the following pieces of context to answer the question.

Testing the picture. Settings Support Self Diagnosis Start Picture Test Try Now Before you review the list of problems and solutions below, use Start Picture Test to determine if the problem is caused by the TV. Start Picture Test displays a high definition picture you can examine for flaws or faults. The problem Try this! Flickering and Dimming Component Connections/ Screen Color Screen Brightness Ghosting, Blurring, or Juddering If your TV is flickering or dimming sporadically, you may need to disable some of the energy efficiency features. Disable Ambient Light Detection Power Saving Mode , or Motion Lighting Settings General Ec
[...]
the adapter from the Component (Blue) input port on the TV and connect it to the AV (Yellow) input port. The Component or AV input port may not be provided depending on the model or geographical area. Check whether Grayscale is set to Settings General Accessibility Grayscale 


There Is a Problem with the Picture. When the TV has trouble with the picture, these steps may help resolve the problem.


Inverting the screen color. Settings General Accessibility Color Inversion Try Now You can invert the colors of the text and background displayed on the TV screen to make it easier to read them. Color Inversion is on, some Accessibility menus are not available. This function may not be supported depending on the model or geographical area.

Question: How do I fix the missing/wrong color issue ?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 13: near_0.98 (train, rungalileo/ragbench/finqa) vs (test, rungalileo/ragbench/finqa)

**A** `e16e7a425adf`

```
Use the following pieces of context to answer the question.

table of contents although our ownership interest in each of our cellulose derivatives ventures exceeds 20% ( 20 % ) , we account for these investments using the cost method of accounting because we determined that we cannot exercise significant influence over these entities due to local government investment in and influence over these entities , limitations on our involvement in the day-to-day operations and the present inability of the entities to provide timely financial information prepared in accordance with generally accepted accounting principles in the united states of america ( "us gaap" ) . other equity method investment
[...]
 . hostaform ae is a registered trademark of hoechst gmbh . mowilith ae is a registered trademark of celanese in most european countries . we monitor competitive developments and defend against infringements on our intellectual property rights . neither celanese nor any particular business segment is materially dependent upon any one patent , trademark , copyright or trade secret . environmental and other regulation matters pertaining to environmental and other regulations are discussed in item 1a . risk factors , as well as note 2 - summary of accounting policies , note 16 - environmental and note 24 - commitments and contingencies in the accompanying consolidated financial statements. .

Question: what was the percentage change in the the research and development costs from 2014 to 2015

```

**B** `152e6508e370`

```
Use the following pieces of context to answer the question.

table of contents although our ownership interest in each of our cellulose derivatives ventures exceeds 20% ( 20 % ) , we account for these investments using the cost method of accounting because we determined that we cannot exercise significant influence over these entities due to local government investment in and influence over these entities , limitations on our involvement in the day-to-day operations and the present inability of the entities to provide timely financial information prepared in accordance with generally accepted accounting principles in the united states of america ( "us gaap" ) . other equity method investment
[...]
s llc . hostaform ae is a registered trademark of hoechst gmbh . mowilith ae is a registered trademark of celanese in most european countries . we monitor competitive developments and defend against infringements on our intellectual property rights . neither celanese nor any particular business segment is materially dependent upon any one patent , trademark , copyright or trade secret . environmental and other regulation matters pertaining to environmental and other regulations are discussed in item 1a . risk factors , as well as note 2 - summary of accounting policies , note 16 - environmental and note 24 - commitments and contingencies in the accompanying consolidated financial statements. .

Question: what is the total research and development for the year 2014 through 2016 in millions

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 14: near_0.91 (train, TIGER-Lab/MMLU-Pro) vs (threshold, TIGER-Lab/MMLU-Pro)

**A** `dcb9f9f369e6`

```
You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`

Q: A 37-year-old woman comes to the physician because of a 1-day history of throbbing facial pain. She describes the pain as 7 out of 10 in intensity. Over the past 9 days, she has had nasal congestion, purulent nasal discharge, sore throat, and a nonproductive cough. She does not smoke. Her husband and children have had no recent illness. Her temperature is 38.5°C (101.3°F). Examination shows congested nasal mucosa and purulent discharge on the left. There is tenderness to palpation over the left cheek and no transillumination over the left maxillary sinus. The tympanic membranes are normal, and there is no erythema of the throat. Examination shows no cervical adenopathy. The lungs are clear to auscultation. Which of the following is the most likely causal organism?
Options are:
(A): Escherichia coli
(B): Staphylococcus aureus
(C): Haemophilus influenzae type b
(D): Mycoplasma pneumoniae
(E): Neisseria meningitidis
(F): Streptococcus pyogenes
(G): Pseudomonas aeruginosa
(H): Bordetella pertussis
(I): Moraxella catarrhalis
(J): Streptococcus pneumoniae


```

**B** `cde05130090d`

```
You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`

Q: A 37-year-old woman comes to the physician because of a 1-day history of throbbing facial pain. She describes the pain as 7 out of 10 in intensity. Over the past 9 days, she has had nasal congestion, purulent nasal discharge, sore throat, and a nonproductive cough. She does not smoke. Her husband and children have had no recent illness. Her temperature is 38.5°C (101.3°F). Examination shows congested nasal mucosa and purulent discharge on the left. There is tenderness to palpation over the left cheek and no transillumination over the left maxillary sinus. The tympanic membranes are normal, and there is no erythema of the throat. Examination shows no cervical adenopathy. The lungs are clear to auscultation. Which of the following is the most likely causal organism?
Options are:
(A): Escherichia coli
(B): Staphylococcus aureus
(C): Haemophilus influenzae type b
(D): Mycoplasma pneumoniae
(E): Neisseria meningitidis
(F): Pseudomonas aeruginosa
(G): Bordetella pertussis
(H): Streptococcus pneumoniae


```

Verdict: real duplicate (same question)

## Pair 15: near_0.96 (train, rungalileo/ragbench/finqa) vs (threshold, rungalileo/ragbench/finqa)

**A** `84a3b7eda75d`

```
Use the following pieces of context to answer the question.

a reconciliation of the beginning and ending amount of unrecognized tax benefits is as follows: .


[["", "2013", "2012", "2011"], ["balance january 1", "$ 4425", "$ 4277", "$ 4919"], ["additions related to current year positions", "320", "496", "695"], ["additions related to prior year positions", "177", "58", "145"], ["reductions for tax positions of prior years ( 1 )", "-747 ( 747 )", "-320 ( 320 )", "-1223 ( 1223 )"], ["settlements", "-603 ( 603 )", "-67 ( 67 )", "-259 ( 259 )"], ["lapse of statute of limitations", "-69 ( 69 )", "-19 ( 19 )", "2014"], ["balance december 31", "$ 3503", "$ 4425", "$ 4277"]]


( 1 ) amounts reflec
[...]
e company 2019s results of operations , financial position or liquidity . in 2011 , the irs concluded its examination of merck 2019s 2002-2005 federal income tax returns and as a result the company was required to make net payments of approximately $ 465 million . the company 2019s unrecognized tax benefits for the years under examination exceeded the adjustments related to this examination period and therefore the company recorded a net $ 700 million tax provision benefit in 2011 . this net benefit reflects the decrease of unrecognized tax benefits for the years under examination partially offset by increases to unrecognized tax benefits for years subsequent table of contents .

Question: what was the ratio of interest and penalties associated with uncertain tax positions in 2013 to 2012

```

**B** `26d398e286a9`

```
Use the following pieces of context to answer the question.

a reconciliation of the beginning and ending amount of unrecognized tax benefits is as follows: .


[["", "2013", "2012", "2011"], ["balance january 1", "$ 4425", "$ 4277", "$ 4919"], ["additions related to current year positions", "320", "496", "695"], ["additions related to prior year positions", "177", "58", "145"], ["reductions for tax positions of prior years ( 1 )", "-747 ( 747 )", "-320 ( 320 )", "-1223 ( 1223 )"], ["settlements", "-603 ( 603 )", "-67 ( 67 )", "-259 ( 259 )"], ["lapse of statute of limitations", "-69 ( 69 )", "-19 ( 19 )", "2014"], ["balance december 31", "$ 3503", "$ 4425", "$ 4277"]]


( 1 ) amounts reflec
[...]
esults of operations , financial position or liquidity . in 2011 , the irs concluded its examination of merck 2019s 2002-2005 federal income tax returns and as a result the company was required to make net payments of approximately $ 465 million . the company 2019s unrecognized tax benefits for the years under examination exceeded the adjustments related to this examination period and therefore the company recorded a net $ 700 million tax provision benefit in 2011 . this net benefit reflects the decrease of unrecognized tax benefits for the years under examination partially offset by increases to unrecognized tax benefits for years subsequent table of contents .

Question: what was the percentual decrease observed in the liabilities for accrued interest and penalties during 2012 and 2013?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 16: near_0.91 (train, TIGER-Lab/MMLU-Pro) vs (test, TIGER-Lab/MMLU-Pro)

**A** `234863e58187`

```
You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`

Q: Following their law school graduation party, a graduate and his roommate were driving home in an automobile that was owned and operated by the graduate. As they were approaching an intersection, their vehicle collided with a motorcycle whose rider was seriously injured in the accident. The rider sued the graduate for operating his motor vehicle in excess of the speed limit. In addition, the roommate brought suit against the rider for operating his motorcycle negligently and driving through a red light. The roommate subsequently reached an out- of-court sett
[...]
e rider offered into evidence the roommate's complaint against the graduate alleging that the latter was driving "at an excessively high rate of speed at the time the accident occurred. "The complaint is
Options are:
(A): admissible under the former testimony exception to the hearsay rule.
(B): inadmissible, because it is considered hearsay.
(C): admissible as a declaration against interest.
(D): admissible, because the graduate consented to its use.
(E): inadmissible, because the roommate is not a party to the lawsuit.
(F): inadmissible, because the suit was dismissed as part of a compromise.
(G): admissible under the business records exception to the hearsay rule.
(H): admissible as a statement of fact.
(I): admissible as a prior inconsistent statement.
(J): admissible as an admission.


```

**B** `d8702005b8b7`

```
You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`

Q: Following their law school graduation party, a graduate and his roommate were driving home in an automobile that was owned and operated by the graduate. As they were approaching an intersection, their vehicle collided with a motorcycle whose rider was seriously injured in the accident. The rider sued the graduate for operating his motor vehicle in excess of the speed limit. In addition, the roommate brought suit against the rider for operating his motorcycle negligently and driving through a red light. The roommate subsequently reached an out- of-court sett
[...]
e graduate's automobile. In rebuttal, the rider offered into evidence the roommate's complaint against the graduate alleging that the latter was driving "at an excessively high rate of speed at the time the accident occurred. "The complaint is
Options are:
(A): admissible under the former testimony exception to the hearsay rule.
(B): inadmissible, because it is considered hearsay.
(C): admissible as a declaration against interest.
(D): admissible, because the graduate consented to its use.
(E): inadmissible, because the roommate is not a party to the lawsuit.
(F): inadmissible, because the suit was dismissed as part of a compromise.
(G): admissible under the business records exception to the hearsay rule.
(H): admissible as a prior inconsistent statement.
(I): admissible as an admission.


```

Verdict: real duplicate (same question)

## Pair 17: near_0.99 (train, rungalileo/ragbench/emanual) vs (test, rungalileo/ragbench/emanual)

**A** `6a733e64f693`

```
Use the following pieces of context to answer the question.

Screen states related to Ambient Mode. Ambient Mode Ambient Mode , you can set up and enjoy visual information and design. In this state, less power is consumed and brightness is automatically adjusted by the illuminance sensor. Getting dark state Ambient Mode , the TV screen changes automatically according to the surroundings. When the surroundings get dark, the TV screen becomes darker. When the surroundings get bright before the TV screen turns completely black or when the remote control or the Bixby function is operated, the TV screen returns to the Ambient Mode You can change the auto brightness setting for Ambient Mode . For 
[...]
ilable in Ambient Mode, which is a QLED TV-specific function. Ambient Mode The image on your TV may differ from the image above depending on the model and geographical area. Ambient Mode , you can view beautiful screens, various visual information, and notifications. To enter Ambient Mode , press the button. To return to the TV mode, press the button. To shut off the TV, press the button. If you press the button when the TV is turned off, the TV turns on in Ambient Mode If you use a remote control other than the Samsung TV remote control, there may be restrictions to entering Ambient Mode Because this function is a QLED TV-specific function, it may not be supported depending on the model. Decor Info Photo 

Question: How can I turn on ambient mode on TV screen. Can you explain about that?

```

**B** `cb9fd1e08e8a`

```
Use the following pieces of context to answer the question.

Screen states related to Ambient Mode. Ambient Mode Ambient Mode , you can set up and enjoy visual information and design. In this state, less power is consumed and brightness is automatically adjusted by the illuminance sensor. Getting dark state Ambient Mode , the TV screen changes automatically according to the surroundings. When the surroundings get dark, the TV screen becomes darker. When the surroundings get bright before the TV screen turns completely black or when the remote control or the Bixby function is operated, the TV screen returns to the Ambient Mode You can change the auto brightness setting for Ambient Mode . For 
[...]
earn about the functions available in Ambient Mode, which is a QLED TV-specific function. Ambient Mode The image on your TV may differ from the image above depending on the model and geographical area. Ambient Mode , you can view beautiful screens, various visual information, and notifications. To enter Ambient Mode , press the button. To return to the TV mode, press the button. To shut off the TV, press the button. If you press the button when the TV is turned off, the TV turns on in Ambient Mode If you use a remote control other than the Samsung TV remote control, there may be restrictions to entering Ambient Mode Because this function is a QLED TV-specific function, it may not be supported depending on the model. Decor Info Photo 

Question: How can I turn on ambient mode on TV screen?

```

Verdict: real duplicate (same question)

## Pair 18: near_0.98 (train, TIGER-Lab/MMLU-Pro) vs (test, TIGER-Lab/MMLU-Pro)

**A** `8a709aa0eb6f`

```
You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`

Q: A defendant and his friend were down on their luck. They decided they would make some extra cash by robbing the local liquor store. The friend didn't like guns and decided to use a toy gun, which looked like a real gun, but only shot water. The defendant was aware that the gun was not real. Their plan fixed, they walked into the liquor store late one afternoon when few customers were in the store. The friend produced the toy pistol and pointed it at the customers and the clerk. The defendant ordered everyone to the floor, and the clerk began to rummage behi
[...]
hile his head was ducked, the clerk pulled a shotgun from behind the counter and fired it at the defendant and his friend. The defendant dived to the side, but his friend was shot and killed. If the defendant is subsequently charged with his friend's death he should be found
Options are:
(A): guilty of felony murder.
(B): not guilty, because the clerk was justified in killing the friend.
(C): not guilty, because the defendant did not intend to kill his friend.
(D): guilty, because a felon may be convicted of the murder of a co-felon.
(E): guilty of involuntary manslaughter.
(F): guilty of second degree murder.
(G): guilty of voluntary manslaughter.
(H): guilty of first degree murder.
(I): guilty, because the defendant was involved in the commission of a felony when his friend was killed.


```

**B** `c6a1f4d3d7c9`

```
You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`

Q: A defendant and his friend were down on their luck. They decided they would make some extra cash by robbing the local liquor store. The friend didn't like guns and decided to use a toy gun, which looked like a real gun, but only shot water. The defendant was aware that the gun was not real. Their plan fixed, they walked into the liquor store late one afternoon when few customers were in the store. The friend produced the toy pistol and pointed it at the customers and the clerk. The defendant ordered everyone to the floor, and the clerk began to rummage behi
[...]
the counter and fired it at the defendant and his friend. The defendant dived to the side, but his friend was shot and killed. If the defendant is subsequently charged with his friend's death he should be found
Options are:
(A): guilty of felony murder.
(B): not guilty, because the clerk was justified in killing the friend.
(C): not guilty, because the defendant did not intend to kill his friend.
(D): guilty, because a felon may be convicted of the murder of a co-felon.
(E): guilty of involuntary manslaughter.
(F): guilty of second degree murder.
(G): guilty of voluntary manslaughter.
(H): guilty of first degree murder.
(I): guilty, because the defendant was involved in the commission of a felony when his friend was killed.
(J): not guilty, because the defendant did not pull the trigger.


```

Verdict: real duplicate (same question)

## Pair 19: near_0.95 (train, rungalileo/ragbench/finqa) vs (threshold, rungalileo/ragbench/finqa)

**A** `41e1220b3306`

```
Use the following pieces of context to answer the question.

approximately 710 asphalt-paving contractors , government entities ( states , counties , cities and townships ) and asphalt roofing shingle manufacturers . we also produce asphalt cements , polymerized asphalt , asphalt emulsions and industrial asphalts . retail marketing ssa , our wholly-owned subsidiary , sells gasoline and merchandise through owned and operated retail outlets primarily under the speedway ae and superamerica ae brands . diesel fuel is also sold at a number of these outlets . ssa retail outlets offer a wide variety of merchandise , such as prepared foods , beverages , and non-food items , as well as a significant 
[...]
, mpl operates most of our private pipelines and 985 miles of crude oil and 160 miles of natural gas pipelines owned by our e&p segment . our major refined product lines include the cardinal products pipeline and the wabash pipeline . the cardinal products pipeline delivers refined products from kenova , west virginia , to columbus , ohio . the wabash pipeline system delivers product from robinson , illinois , to various terminals in the area of chicago , illinois . other significant refined product pipelines owned and operated by mpl extend from : robinson , illinois , to louisville , kentucky ; garyville , louisiana , to zachary , louisiana ; and texas city , texas , to pasadena , texas. .

Question: what percentage of pipeline barrels handled consisted of crude oil trunk lines in 2007?

```

**B** `d7a2393c6d6d`

```
Use the following pieces of context to answer the question.

approximately 710 asphalt-paving contractors , government entities ( states , counties , cities and townships ) and asphalt roofing shingle manufacturers . we also produce asphalt cements , polymerized asphalt , asphalt emulsions and industrial asphalts . retail marketing ssa , our wholly-owned subsidiary , sells gasoline and merchandise through owned and operated retail outlets primarily under the speedway ae and superamerica ae brands . diesel fuel is also sold at a number of these outlets . ssa retail outlets offer a wide variety of merchandise , such as prepared foods , beverages , and non-food items , as well as a significant 
[...]
l operates most of our private pipelines and 985 miles of crude oil and 160 miles of natural gas pipelines owned by our e&p segment . our major refined product lines include the cardinal products pipeline and the wabash pipeline . the cardinal products pipeline delivers refined products from kenova , west virginia , to columbus , ohio . the wabash pipeline system delivers product from robinson , illinois , to various terminals in the area of chicago , illinois . other significant refined product pipelines owned and operated by mpl extend from : robinson , illinois , to louisville , kentucky ; garyville , louisiana , to zachary , louisiana ; and texas city , texas , to pasadena , texas. .

Question: what was total miles of private crude oil pipelines and private refined products pipelines?

```

Verdict: same passage, different question (removed as shared-passage leak)

## Pair 20: near_0.95 (train, rungalileo/ragbench/tatqa) vs (calibration, rungalileo/ragbench/tatqa)

**A** `01ec2d3d3602`

```
Use the following pieces of context to answer the question.

Other identifiable intangible assets were as follows: [["", "", "2019", "", "2018"], ["", "Gross Carrying Amount", "Accumulated Amortization", "Gross Carrying Amount", "Accumulated Amortization"], ["Non-amortizing intangible assets", "$3,678.0", "$\u2014", "$918.3", "$\u2014"], ["Amortizing intangible assets .", "1,244.2", "260.8", "576.6", "212.1"], ["", "$4,922.2", "$260.8", "$1,494.9", "$212.1"]]


Non-amortizing intangible assets are comprised of brands and trademarks.


Amortizing intangible assets, carrying a remaining weighted-average life of approximately 20 years, are principally composed of customer relationships, and acq
[...]
 changes in foreign exchange rates.


In fiscal 2017, due to declining sales of certain brands, we elected to perform a quantitative impairment test for indefinite lived intangibles of those brands. During fiscal 2017, we recognized impairment charges of $31.5 million for our Del Monte® brand and $5.5 million for our Aylmer® brand in our International segment. We also recognized impairment charges of $67.1 million for our Chef Boyardee® brand and $1.1 million for our Fiddle Faddle® brand in our Grocery & Snacks segment.


Notes to Consolidated Financial Statements - (Continued) Fiscal Years Ended May 26, 2019, May 27, 2018, and May 28, 2017 (columnar dollars in millions except per share amounts)

Question: What was the accumulated amortization of fiscal years 2018 and 2019, respectively? 

```

**B** `c3119cd120f9`

```
Use the following pieces of context to answer the question.

Other identifiable intangible assets were as follows: [["", "", "2019", "", "2018"], ["", "Gross Carrying Amount", "Accumulated Amortization", "Gross Carrying Amount", "Accumulated Amortization"], ["Non-amortizing intangible assets", "$3,678.0", "$\u2014", "$918.3", "$\u2014"], ["Amortizing intangible assets .", "1,244.2", "260.8", "576.6", "212.1"], ["", "$4,922.2", "$260.8", "$1,494.9", "$212.1"]]


Non-amortizing intangible assets are comprised of brands and trademarks.


Amortizing intangible assets, carrying a remaining weighted-average life of approximately 20 years, are principally composed of customer relationships, and acq
[...]
which were caused primarily by changes in foreign exchange rates.


In fiscal 2017, due to declining sales of certain brands, we elected to perform a quantitative impairment test for indefinite lived intangibles of those brands. During fiscal 2017, we recognized impairment charges of $31.5 million for our Del Monte® brand and $5.5 million for our Aylmer® brand in our International segment. We also recognized impairment charges of $67.1 million for our Chef Boyardee® brand and $1.1 million for our Fiddle Faddle® brand in our Grocery & Snacks segment.


Notes to Consolidated Financial Statements - (Continued) Fiscal Years Ended May 26, 2019, May 27, 2018, and May 28, 2017 (columnar dollars in millions except per share amounts)

Question: What do non-amortizing intangible assets comprise of?

```

Verdict: same passage, different question (removed as shared-passage leak)
