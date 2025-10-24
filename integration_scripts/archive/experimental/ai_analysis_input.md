# Phase 4B-2: Intelligent AI Analysis

You are Claude, an intelligent assistant helping reconcile 195 Fathom participants with the ERA Airtable database.

## Your Task

For each participant below, **MAKE A DECISION**:
- `merge with: [Full Name]` - if this is an existing person (use exact Airtable name)
- `add to airtable` - if this is a new ERA participant who should be added
- `drop` - if this is a device, organization, or clearly not ERA-related

## Guidelines

1. **3+ Town Hall meetings = probably add** (unless already in Airtable)
2. **Number variants** (e.g., "Joshua (2)", "Joshua (4)") = same person as base name
3. **Jon Schull variants** = merge to "Jon Schull" (that's the user)
4. **High Airtable match (80%+)** = merge with confidence
5. **Device names** ("iPhone", "Galaxy") = drop
6. **Single names in 3+ meetings** = check Gmail/context to get full name, then add
7. **Read the actual content** - don't just look at counts

## Output Format

For each case, provide:
```
CASE N: [Name]
DECISION: [merge with: X | add to airtable | drop]
REASON: [brief 1-2 sentence explanation]
VALIDATE: [link if applicable]
```

---


## CASE 1: Belizey

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/165893831

---

## CASE 2: JP

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...jIWRh6w4vmMx7e7nD3dIWbuzNcXJ36haG9oy1s9bLQZvs2WNuwMLSAJaeqLMyxZesmbN6ysZ/H9y8IhkrA78NQQfhUhkhCU0yl4WBx+IoQhxKDE4YDpUuNS5j2S0NTcfgdYGkoicPLeOuhEY8kYSiJQkkQGvM28ebDK0IifvT2fbx+/zJ2tVcjMToAoSoPhPt7Q+XlhB3Wm2C1YSXstm7A2iXzMHHkc3ju3/8Nz//w3zD22Z9jxsujsXD6FMybMhGTXhqBcS8+h4mjXsTkl0bS7ZGYOoal2XgpqTdpEiaPHo2X9eKQU3gsDg3Jw+d++CNRzlPqL/g8Jo4YhUkjXsK450dgzC+eFwJx3Avcc3A8Zo43yLdxmMn/JzBjFpbMmSek4eI5czF32gyxnmXhVLo/33fmxEkifbh+xUpsMFsFs4WLxeO4DyJv5/vOYREoJOAsel8zMGfSZEwbMxbjX3iRXp/e28iRmDKaE4Mv03sfJ2ChyAlELk/KzJsyFdPH8b6NESlL7mO4btlybKTXXLt0ORbPmiP6Lk4cNVqIVJaVE1kuTpyIlQsXYPPqldi6ZhUs1xLrVmHzqmVYv3S+6HW4YNo4rJw/Dc5WG5FG59TuhlKc2NeOS327aV5ykOYyx2hOw6nDE0Ii3r14WAjDW1y6lEuWCg4KWCJe18vDIejl4UDJ0gEu0O0LJwZEokEW8ihuE0IeDhGGJnDfQy5dyglEgzw8YJCH+r6H+t6HLA8HZKGh56FBEkrSbzD6tCDBcs80KfhtDBKDndUSHXr0t/d31giGF4dDexuasodpr5IEol4i7hJUYGe7XiIaEEnEUkkeCoFokIcD9ItDo7Klpr0P+wVifw/EAYH4bf9xLUnDf4rDvxdx2F+S8f+DOFyycr6Qh5I4nN8vD1kYCmkoWACzjbRuk5Q65MThKj0GcbjGQhKHkjxcKsTheks6Joq04VJstVkDN5qT+od40XWGlDYMDVcgJEyO8HA/RND8NyJchUCaY/**jp**/2AxMECOQH85lHJP+PIfOBJ+tKz280EQrQ8NUtB2XpYhOTEKlRV5aG2tQUNDmZCEeXmp+v7qOTQ/yKO5Av/hYSmamyrRQjTUl6OsJA9pqXGIjgqhfQgUiEoqoTy34XKoQbSPaihof1gWCmHovUOUMO0XiXI3eLJMJAylS1kcOnH5Upftg+Shtf1mWNmZ98vDLaJs6TpRslSIQ3O9POTSpaJ8qRnWsjjcwKMRBnn4fcShUQ/Eb8JUGj5dHpreXjSIbxeH3yYPhwrD7yQPB/1GTKTgN7FkqDTs72VoKg2fJg6HvL9/IHF4oDkZzSUayNzMYU7/aFeZb8DCdRvhq03EoWsPcODCbeTXdiImrRhHTl7HJ1/8Cb/6+Hf46LM/4MNPv8Y7736A5uZW1NIk7/LV63j/Vx/gq88+wYevP0SeNhCpqh1oSw7Are48XOnOwMm2WNw6ko2zXTocrFHjcLUaPdlu2JXjjqNVKpxrj8D5rkjsK5ejM8+d7hOEe31FKI51xMaZP0OW/ybsLwnE/opwlOhcILOaCx+reUgMskNqmANSQmyRHmqH7Ag75EU5oFDnhHyiLNkblel+aKHJ+5GdFfj43dv48tPX8OXnb+DLL97EVyKB+Ba4l5/EOwN8wRjk4QD/eOJwOGGo73H4GYvDV/DVRw...
- **2025-05-28:** ...BJKB8Fnmp9B6dwVCzB0/DADUo0aHcRz4qxFs7D9wHYciTiGFetXYuDIQX8CUoPSm8UylE+1rmFN90mIOoLD+zZh3dLZOLw1GElhe5Acvg/JEfsZB5BKsMxLiCCwCUxjLU1flkNIFJTmxKHIoFRzv6Ptb4Vp0bzYHkP0qX04xwv/3j0bsYBAGjRzEtYsmYUtJOrQlfOxdc1iQukSU5/2bVmNA1vXIOzAZkQd22mgKM/EMgEpt1EdxgIN1RkanGpMYm6MQWm1mj6KYgibCXioFOz1Aty7nIGaS/K8jCOUphL2CvCcxADRHgAAgABJREFUF9uH1ZdQLZWwOMV8L+WNqWabIkZxxjlLwbpD6qNGP5bmRHMbzvNiHGcTc5TqFtjeLHOrjU5Ul6cRfjLsIv/yjmZ3V5oVkmo3VYspo3yB4ANTStVhrGk2Wdbw9OiGk8ZXCEqfVBNsb18kZMj+ybGGkt+k7IwqCmOtASU32TFfL0gJNyCtKJCCqDR8himbAkvVnaqeVj9rwo9gVb9/eksd/ersv+SyoFKN6aVaALWoFtRdMDDVz7crMwknhL+ieNzle9WIVJUwqIZR6XsHTJXCdbrvZSl1n9D7guD0nCEw1vz5i/xMk88fI5yF2UQnpYg15z0vWUrpWYNSqaWOSprwBZBy/xcJVOP/AU4VVQz353G9WDWl6WYdJXC9XBBlDWD5aWcQeXI7YiP3GWzGhB1AXMRBM3F/eLWIMFiI62XZhLMYUwlzEk5b7aOanvJSomxk7v7t67iIWoWdFiFcTK3D9vVrsGXNSmxcswJbN6zGvu3rzQhfwFuYqgELCSjmQi4vIxYZhNP02AikMZKjTyJeTYAxJ6y2tuJCkg1S0D4TxKtOWWqzQjXMqmf++f0d/PLhLn7irf7ulE44QPrNsyqozKKGz5F2/jjCj2zj9iyD75ih8OZKt3vnjpgwpA9ObF3BBYuaAsvMTkxNezVXsm0c6dUSGedfNABVg1il7Ll4vhCYVvKcUXWJx3hFHqqK0kwtFZhqpK6a+D69uoMfCJF//e4F/vbDG4PSXwmk8hvV9CxN0vr4THXZj/Efv2ok6U/477//**jP**/62y/4n//+K/6v//gN/+e//4z/+P17/P3Xbwm0H/hcBNdvX+DRw1uIiQrDpJH9sGK6D7YQDjYtm4R1S/xxeMdSJEXu4IL5CCpzDiMjcj3Ct83B2d2BOLU9EBsWT8AwQuAAguGI/r0wy28Q5o/tj2mj+mI2QW7JxGFYNmkElhLy5owegClDemLJhIFYNXkwlk4djJUzhmLZlIEYrmam8aPgSTjtOV5d4cPg5T8SPeUtKIXDdxi6Dx+ADv16Edq6GJAqfd/Yw7GGattXNVmKbmjl1ckAr2Gn5o5XaWunyUjNRnXUwU5AbMyLVfNOUv26oUNfXgz6a+ygN7pxG3uOJ5T6E0onDoeHC0y7cfu68kKmhieZ+bcboE5ZjTXtaAAn5bNR2+a8+Ki2VDDayKJBU9WZOsb6BqXy/dSUJIKmwLRZ59ZmVt+8u2Og71ZK5WMqWybBpBqp3Cb6TnlAQ+uqlzF+S8221/vo2s5CtaVSVk2NVU0o/1cQrltBqYegdIgmz3ih8yBP7q8u5tfaRk1QulDKnoagLSCWr2qdVqqDbWajT+X/KssqqapeXHz052c6fPZ4DCOYDgzQ4IFRjJHm3+i3aDImLp1mUDqekDp2xmiM8R...
- **2025-01-08:** ...2Bx75DCDthiFQTS+Ra2aHBPwi6sEh0RUYT1uIwmhCPufQULGalYTknnZcLmWmYpWOzaak8c5SlrAyeUzk5WM7KxlxqKqaTkjGVmIQBgmB3SCi6QkLQERRECURboD/agvzRGuQHXZAvQY4hzg1Vnk4o9XBAtr05XPa/AMuXn4bx7mdhdehluNKXCTfTk3Az04e7pTE86MtDhI8n0qIjee2boqICpxeXCGSXCWJXcOUyA9trBDiWV/mak3yWewa4y1SyObfWTuESb0Zlk6Ouo+3iOVy5sCaULGxSVT4nl1ADd35tkTefvvYq6xu3QsBbr4G7wJpXGeCmNyffXSaALS2yiX/H+dqowtJZE3zVBVYyhPHt5Uk+gIHNA3eGN4GNbAJuZXGc338jrCZPyOhm2LqqG1lka62uZ2F+8JZsv0DdbZkYH13PGKGZZZxAt56pMULd7cNum5wavXMmR+kx/nczvJ4RzE6PEtjHCFLj8PH0wEMPPoh7v/pVWJgao766AjMTw5ShzUyPD2B6Ynv6MDXeu54eSjfP5FjPLZkY7d6SLkrnZia3ZYoQNjXWzTNNmdkauu/MiJDp4U6eqaEOnsnBdp7tz//dlu1Qu1M+B7iNwQsbeGtbfodnK+Ba52+F3O0A17rwJrRz16AhvLE5xNRj56AcXEJ9/xwqO0Yh1fajpKkdxSodlRoUN6hQpFRCrKyj1CK/vgqiukrk1VVRqiFS1CC/QYFCVSNKmzWQaLQob+1Aha4TFdoO1Og6UEvbitZO1Le0oUatQX1zC+pUBDiVitKImvp61FKUBLoGSiP9PIVSwVNP+3UKBSpr6yCtqEahtAK5JXJkFbGLvQwZReU4ZGSL+x99Dt7h6YhJL8fuo/YQiRXo6ZrlgBvrmsF83ywuTqzi2vxlvHfpXQLcu/j9azfwx9d/gw/e/**jP**+/tP/xIc//ws++TUB7sYnHGsbNWwb23yfo47Vwn3E8fYxYe4vv/4rFifW0NM6ga72WWg1k5DKO1BY2oLoJAl8w7Lg6B2HL3yVXtwf74WDfzJMXSI55Kw9WaJh6xUFa49wWLmHwdotjBAXBDOnQIIbw1sA7YfA3jsGroEMcNkIShAjIb8GOeUaFNZ3oFI3jNq2USg7xqBsH0ZDax+U2nbUq1sgr65Fmbycr+uYl5eDDAJcclw4EqOCkBDiRYBzQ7SvI6K87RHhYY1QVwsEORkjwNEIvg4GcLfWg5sVm6pBDy4Wx+BgegS2FDvCnL35CdixWOrzONiawNnBCi5ONnwAhBcHnD/8AgIRTBCIik9GXEoGkghvSdkipOYXI10sQVZxOX8tM4srN5NGiEvOl6wDLhfhSRkIIsD5sgmGA8Lh6h0EOydPODh7wdbB7XNw+28JuE+AvxDgTp+5jBVW+7ZCcOP94FbBV15YX0qLA27lDCYmZ+HnG8KbUF8ktO0ktL343C7C2x7soe29z72MfZQ9z77Ia+H2sBo4BrgfPonDTz4Hvaefh9Wu/XDYexheh44iysAYyWZWKHJ0Ra1PADqjY9ETE4fB2HhMJCdhOjUZKwSzM3lZOJ2bSUDLwEp2BpazMwlzDG2ZWCI8naL903R8LS8Xq4S4lYxMzCUT8pKSMBIZiYGwMPRT+kJD0RMSjE7CW2cwQ5wvdIE+UPu5E+BcCHCOHHBZ9mZwPfgSLF96GgYvPgVTwpyj4VG4mxnAzdwQrlS6Wpgg0NUZCeGhKKH3uUZRT/BZJIhdwVXWdEpo43lVqIG7enUL4FhJaLuwuoLzq6cIbKwm7hxFAByrlWOou3ieoW0jZ3B2dYEiTOTLIjSfbvSBE2rntgKOhdXEsabUzdUZ1qcOYYDja6ASxjYAxxHH+zGNCjVsiywCAjcgyDHIHvv/Au5zGRsdwdjYCMbHRjG+DrkJDjmW0X8atvbtP834/06GNjPJQEaImxgb5IAzNzbCd759H7734AMwMdBHhbSEADVIGdiSfkofz+RoP4XKsV4ho71bcCZkfORmxghaN9NBab8l41syMdKxmcnhz2cDbBtomxhouyXbn/+7LduhdqdwwDG4bWQDbxtw0y2+JWThbejm3oJ29mZ0829Dux6OuM3QsbnrfA1NjrfxS6jtW0Z5+yTKtMOEMTb7fzOSSquQWFKOuEIJ4sRFlELEivMRXyRGYmkRkiQlSJaWIVkmQ4pcjiSZnMoKZFbVI6taieyqBuTVqiGqbUJ+TSOK69UooZQpmiFXNqOioRmVDQS4JoY5DRSEOiVtN6g0UFGpJnSo1M0UNa+pUzSpUKVQQl5bD0llHTLEZSiqJDRWNqCSsHnPF...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/121641973

---

## CASE 3: Jeremy - Open Forest Protocol

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2025-04-30:** ...we are looking for collaborators and partners to grow and multiply these models together, for questions please contact us 

	rolandeansima9@gmail.com here is mt email, or you can also visit our website  here https://folonahub.org/

	

11:07:48 From **Jeremy \- Open Forest Protocol** to Jon Schull, EcoRestoration Alliance (direct message):

	www.openforestprotocol.org

	

11:08:13 From **Jeremy**...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/289548672

---

## CASE 4: John K Carroll

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/50542167

---

## CASE 5: John's iPhone

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-08-16:** ...Thank you all, I will leave at 5pm, wonderful to experience ERA in action with so many amazing and committed people\!  
17:00:49 From Natalie **iPhone** To Everyone:  
	Nataliemariafleming@gmail.com  
17:01:53 From Katrina Jeffries REDES, Senegal To Everyone:  
	Thank you all for your passion and information.  
17:02:21 From Jon Schull, EcoRestoration Alliance To Everyone...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/223525279, https://fathom.video/calls/189386729

---

## CASE 6: Jon Schull (Enabling The Future)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-04-30:** ...and save the date for next mini workshop, 9AM Pacific on Wednesday May 7th with Brock Dolman on the Fuels to Flows--"gully stuffing"--project. (**Future** workshop with him will be on the power mapping they did to bring beaver back to California.)

	

09:22:36 From Jon Schull, EcoRestoration Alliance to Everyone:

	https://docs.google.com/document/d/15ZHtbMsMvta...
- **2025-03-19:** ...The Big Map](https://experience.arcgis.com/experience/40da4f30e90f4578b84cb9f4353308a6) | [**Donate\!**](https://opencollective.com/ecorestorationalliance#category-CONTRIBUTE)

# Master Class **ERA Town Hall Meeting \- March 19**

## **Meeting Purpose**

[To discuss the **future** of global ecosystem restoration efforts and explore collaborative strategies for the Eco-Restoration Alliance and Global Restoration Collaborative.](https://fathom.video/share/8FMPzU-SGoe3phszNqWocaRQScEx-u6z?tab=summary&timestamp=0.0...
- **2025-02-19:** ...Would love to chat more about creating a just, regenerative **future** together. We work towards orchestrating funding, knowledge, networks and talents for regenerative agriculture, ecosystem restoration and transforming food systems (to name a few)  
	  
	Please feel free to reach me at: aditi@amped.nl  
	  
15:55:37 From Jon Schull, EcoRestoration Alliance to Nadja (direct message):  
	Are you good for...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/331536869

---

## CASE 7: Jon Schull, EcoRestoration Alliance

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-04-30:** ...10:08:41 From **Jon Schull, EcoRestoration Alliance** to Everyone:

	https://permacultureeducationinstitute.org/morag-gamble/

	

10:09:20 From **Jon Schull, EcoRestoration Alliance** to pedro (direct message):

	Welcome Pedro\!  How do you find your way here?  (Have we met?)

	

10:09:51 From **Jon Schull, EcoRestoration Alliance** to Everyone:

	https://folonahub.org/

	

10:11:48 From **Jon Schull, EcoRestoration Alliance**...
- **2025-02-19:** ...it's during sxsw  
	  
15:23:14 From **Jon Schull, EcoRestoration Alliance** to Everyone:  
	May 10-14 in Vermont with Didi\!\!\!  
	  
15:23:35 From Johan Myrberger to **Jon Schull, EcoRestoration Alliance** (direct message):  
	great to be here, but I need to leave as mentioned in the main chat  
	  
15:23:46 From Mark Haubner, NY, Bio4Climate to Everyone:  
	Replying...
- **2025-02-05:** ...https://forms.gle/eJJc1659JNpH7Qds7**  
	  
**08:15:48 From MOHAMMED ALKHALID to Everyone:**  
	**I’ll disconnect and reconnect in 20mins riding an uber**  
	  
**08:16:46 From **Jon Schull, EcoRestoration Alliance** to Everyone:**  
	**PLEASE DO THIS: Please contribute to the "joint ERA LinkedIn graph": https://forms.gle/eJJc1659JNpH7Qds7**  
	  
**08:17:19 From Richard Tusabe to Everyone:**  
	**Great deliberations team.**  
	**Thank you...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/408247629, https://fathom.video/calls/319553577

---

## CASE 8: Jon Schull, EcoRestoration Alliance (2)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...OCquw4uOh+hNMYEXYUeqM90h6/1fuxd9yJs9fYgKZQdqz4TrWVx6KlOwuyREpwYLEFNtheaiwJxcrQU1+dbcPv8Edy9PIbbxJVx3L1+DPdvTuH+rSk8/Hgan9yexaPbJ/DpnQU84pxknMKje2fw6P4ZPGTjLx9dwtdfUYlTSfpQLA5l5aH48t+SOPzq0yv49tNLbNLajYpEL0RbqaLY0wBN4XaoDbREfbANF4d1gXZooH4wJA7DnNAS7oz2CFd0RLqjlSFJG9bE+aE6KRRJ/m7QUNiF9W+9i03vb8SG9zZh/ftbeG/DTSQOuTxk2+vksGWDPEMRWzaqiFFmiMUhScONlDZU5vKQUoc7tx3E7l1aUNytCxVlQw6Xh/LaPH2oJBaHijx9qMtHSh/ukdfHHgUDKO7Vh6qqIfT0LOFi746kiFiUZWShMC4O6WwhnuTnjWhPTwQ5u8DTwQkiOzs4OjjCwcUV1i7uMGPoOrlA1cYOe8wtsNuCMIeSuRk02e+bhYcLnHzc4envgZCwQHh7e7MTmB07GVrB0sQK1qbsREpS0IbKljpznGyd+GVXe1cuDp1tRHCk0qYW9nA0s4etgSWstM1gftgMVnrWMGPbZtomsNRlJzNtfZhq6SDA2RmJwX4oTY/G57fP4J9+/QBffXl7idRaIsl+CKuIsb82/uLiUCINxZzi4pCShovikMvDVVKHy8UhbUvFITvG90lDoQTpKqKQy8Iy6bhwtFQKlShdkEjDVZKGxJxYHM6MFGByqIiLw0g/B3jYGsDBhMShCvQPKODg3i1Q3vEh9si9xxZTqZgeysPMcB4mj2RisD0WR/uSMNaXjOOjObjGxWEjWxCX4eJ8BU6ML5YqJXEo4cRR2dKlQuqQxCElDk/xxGGeWBzmSsucEoJIZJfHKbVI+wR5ODtKl/PZfYrZYjkXRzoS2IK6gPc4JHHYUumPxmKxLGTUFnoyvFCb783ThoI09EBlrhf0d7wCS0ocbl/LsZB7DcZbXoadwltw2vs+**2**/cGROp7obtnB1obKpAcE46OxipkJsWggE10afRysUZGYiiiglwR7GUPf1creDmYwMPGEElh7LvD6DBM2ATUUksFLqaHkeDtgPQgN2SFeCAv3Bvl7L4NWXHICHZFaUIg245GbXok8sM9kBPmipxgEQoj3FAW6408tp0b5ISCYGcUhbqgJNQV+exyjr8DMrytkeZpwUZLNpog1d0YKe5GSHI1QDLhYoAkF33EOeki0kEbITaHEOqghxhPS4Q46iPA9hC8SByaqsLPVgO+NhrwsDwIFwtViMz3w8pwLwy0d7IFw262cFCGmck+mJiw0UwZtrZqcHRUh6NIg+PioYPQCFsEhJght8QHHWPJ+PR3c7j2xVH8Ix7i5ldjuPpZLy48ase3f7zGrjuJa1/3scvd+PTXl/Bv+B3jn/Cv+A4Xb4zj1KVBTM53YXKhHrNn+3DsdB/GTvSjpKYAJ2/dwNytW+ifGEFEjAfc/UxR3xePmiMBaBlLRNdULY4tDCI8IgQBYZQqdIVLgAgWzvqwtDeAh68veocHEB0TitrWGnQMdWP61HFExoWgoCYH1e2VyMtPhLebNTw82MLFwxYxCZGIiI/kf5np7++KMPazCgwSwduLFlm67HtfFyJDNbgaqvJ+hv5mVLJUEId+pupcHDrrKbHrVeCsvx+27HYd3dWoqs9AW9dScbhYplQoVTomThuSMJRIQ0EctuHoVCvGKHlIJUjF5UhlexsKlzvZSJe7OJQ47OkuxPhYPcZGajHYXyIWh2U8cXic5ODJpeKQtmdP9XNxOH9mGH1DVZiZp8ShUKpUgNKEJA+FcqWygnC5NJS9bkWKcDlPShUeUl0hCB8nCg20D8BQ++Cq8KQhu42eGKk8lIhDPYk4pMQhycNDYnEoi1gcMkzZQltWHlpIxaEYC31YcXloAGsrI7Y4N4G9rSkcxOKQy0Nx4pCnDWXEIbEkbegrkzaMCkBsXDASk8KRxuYVuXlJvLdhVbWQNmzvqOFpw5GRDi4NJ6eO4PjMIGZmhzA7NyyFBOLkVB+OHqXSpdT3sAG9vdXo7CxHW1sxWloK0NCYi/r6LC4Pa8TysLIiRUoFlTAtTUBpSQJKiuNQXBiL4oIYFFIJ08wwZKcHIzM1EGnJ/khL8kVKojeS4zyREuuB+AhnxATZIYHNZfMinVHPzl89OcEYyg/FUE4gJildWBWHc4zzFbG4XB2PK1XxuFQWhfPsunP5ITjPuMAgaXizlKRgDO6y296vjMUDdr+HNfH4pFbgYU0cHtSw66pjcK8qGncroxg00n1icKc8mnOPbd...
- **2025-06-25:** ...tixLHlMTxSMIvoJQeAL3tiSptV22J6KglPTcFnVFmvyvm74rYCREzg8aauRUZRA5qv+wPVVuj3mdDi2GqaEAoDyrZQfF7A9XroOqcRRkzL8YXxYQ/ntyVUi8k9HMxg8rXYuhl5MFpgIOIGgtB60rilpL4uQRuWU+sqrAtIAyUoEIlRx5EJMxqHOuO45agK+2PNu6vvQl985DNfwhbicVR1IRuorPNJ1hmEqyT4DE09EM1M63iAEqWoNPFYcuxFjcoiuiOfuGfE0XYBoA+6i9AlmkrGuuyifAl4OsGS1hndemQOpoHQIwjI3F0GHAzhpoVUR6g6hhsTUxvIPay+SWWTTW2pyfCOmxJh82YyEU9OBNrtMsQbtnlEDDHPwDWfplmFLBIP1ozmVpEdAXehvAgBRhN0UnTwlo03heQ2ZZU1KKcnJHYJuXkLGAE8mDQtakNMFQXgQFYeMUc6v4izgN4/Yt54EP04Jjl6LNYBpcFKA99QcZ6DqRPHciaOJgxEZf+CFqC3D4lF+aiLWcBkOsQ5TpIeA8RaB8eVAULUM56wZvB0aIGh3XvF4OCAIYr19Be6FxJXCiJCSeSYTMVRB1fWNaw0QyfbVmBu5COAnoAHSiAAWN5UWUVEdba1vS2SAK5qsfdSmxSTT3UCTNKZkZNuMwsOhR0VTRxlZozUot62q9lohPWWPAYgG7bEgwVWqDUteBVO4LQsxQM2pMUYryGc8EFaNEY/XY8hR5WdIUONHPTRC4n0T49tpBgX9Txcyi/i0rKQPBs7de5ApuiCSj8JtCSyOmKdT6KdTyQpE+jAbhoPZOGC0e7PFzPhpYNaoQJpfOO1Dktdi5JHC6ZfUnDz0J3Bpcld87Jc8MHmPn4qyuxzLTRPpXATpuZ5RQhqGfmIHwYuHU0a55a1LEzJmHGxM8aGa+RWzE5vOBykcAgdrTUupZB46RorBDYlIsgiGR3pcwW9EdoAOBzEuD+0+uJ+J6Z2FPTYSXnRzUqjEsneBIyg6Z0H3gbJb8E3AkGIKsQXEreA+IN/inNmovJfCDOvK+6Nq3OWkD5aTas4BFcxjsQYEnTl0CFquBX04+11FMAuP8esP6RsdTsslF4kP7wp4xHb88U3km0jwBXGYlJEzWR4hwyCU3k+HJZ8PWnVROKtA4zNWPA5rTW+wn80KfV3YXuFefE8rGstsP8AyMxBUyWxHd/XtletORLv7eouFR0hJ9Au+5wVSeu15T73jru7J2+ek9r6Uxiu8xMw5ncxhvht1iPL5XrS6WHk8keA1YijC2VLj07l9tntLam0N1JTBM3spI7vXYuv8tItCUy3UfS27nb7vRHy0nOqkT6DgIs6NgGejwxo+GfWvqK/HvJmY1AfAlMv4G+QY94rk2tH3E2JAA2WtoSyQZuyF+**2**/PwwX5dCdxwTBjSX6k5nddeH/3L55pz6cg3aTxBv0dtqAOuat/75i8qRVL7zOH/PcKUPgCzJXlniW3M8WDpiv5mED57kluP+qeNIRveZksYc91JpIKJMK0/A+48K05rLw0nMkJ5Ei4kVuDZ+33bXwDabqPuyb+6pLQ8l3w3IbR3HC+4mZ4/FWm/G4QNS6oGacRuYFYj6ZnwqiehPoRsPU6UpZEGirdiUVqVPazRau034LT01piTvKqlHenoRoiw44hjSdYBd+tA+HcOOyohuxVc3jtk6T9h69F+16W3DGuyh1rastfpUmCtalAAOa15BzKqIGei3CeSk2TpmsgyYLd2JeFcS2W4k+1TEfRk2L7P6UGU96UYjSvRcHLUECh7gXUqDQ5/QskM6stNo60yle1KI+sNkcxI5JPt2JMkBTnAB/KaImRexC6guhATdHwQ9jRYGBLCjJnR8v56+acD7TNio2XJff+WBzjoN4R9YEORpHP46Dn8rwp5AGFCQM1p8MpnxJ9gWzWl3DtuGj2ODR7CRxLS7urSHSmwOQDOOQ/O2aJInzQAAgABJREFUPuTdH7LhWPqxhHoC0AYEZsK8CaQrgZpPICeAxPW2nmS6N4nsTMI7Uom+o+TICfLeSWwyFVsAdEP+GnFJlHvoNR0FD2IhGXuYartzzDoGZ0zBhxKoW3p2QMXfkgrj8cI9GX9PzU7omAkT89BMR42dUGC3tfy0kprWsktJzhBgq4l8ZMK6DnPQlAfNzJ1EdlFP+jRYxMA9VVE7KmoLTvfz7KHo2BYAlpL0KYiAzPpEgb1QMpvIWduHtHx7gr1PR/aaiNtmaspAzBkZv5HfUuPbOtue1vYkWsm0I2Y3xey6hImAojWS7gRiNgWfOEyMp+AjSfgA/IQk+nYKPpeAedHABLuOxsWoWYhhAJ0Kiw9IV4kK...
- **2025-05-28:** ...**2**/RfW/9OZ/zPk/y0BgIWZu4CU+c/**2**/56wsJQJ4l+A7f05658FALbTAgB2AZgFe7bwZ1t/tve/HVZO3rB2YvLfB5bTcJZI/hmy39ELVq6+0jq3BAtXWp6y+bdy94WVB8FTCWsZW/5P2f7L2To9ALaKANh4B8LWNwi2LABgBwD/UNhz5n9QBBxVajhw1v8U8e8UqpUI//AoOEXEwFkgmtaj4UKtqzoGbgLRcNPE/H/svQWUHNe5NRrLju3YlkkWDzNzDzP3QA/0MFMPk4aZmUnSaMQsW5YsWWxhJNkxxsxMN07ikOPYlmn/33eqh2TnJjfrvvfWe0+z1l6nqAtO1ak6Z/b+9icwT/pLcImOXUTiM1ypM+sSQ9sqlXAUVv7RwuZfWP3PRfkzWUzbx/C2ElxjqWQwmRwfOwcX6mg6x0cLOMWrrf3Z6j+Rbfuj4ZasFKWw8udpNVxmkSLBNTUGbmmx8EiLEXBnpBMyaJ6RzstZDBBJZRStj5SQHiHgRnBNV8A1gxEOt0wF3LIWwz1bgkeOAp65EQJe+RHwLYqCf6kS/mWxCCiPQ1BlIoKZ/K9PgrwpBeFt6VB0ZCCiIx2RXZlQ9uYgfjAPicMFIuI/ZawA6eOFyJgsRsZUMTLXS2XGVBEto3UT+Ugdz0PqaC5ShglD9Jv+QiSzCKCnYM4NIKYtD8qWXEQ3qRDZoFKnA8iW0gFU0IC8PEeIAOZSAhRlwL8wUy0CSBUiAK+MJHinJ8EzlUUA8fBIioX7IhGA5ATgKEQAip8XAQTOOgEw+U/wCYK1D7tW+MPK008IAWy9/GFDpSWLANSwcPdWCwDmMUv4/xxYAGDh6QkLFgJ4LgYvt/KahyUv83KnduMGSx93ajtukl2nnyssA9wErAIZrgLWQS7UjlxgLeBMbYkQKkFE/oc7wkZBiJAJJCX/nAAgVg1JBCBF/icL8l8IAJj4z0tDSUE6IQ1ldD/WlWahskyFqvI81FTko66yEA1VRWhigr+mRKClthRt9eXoIMwKAGZFAE2VBXMCgMXIVQsC5t0AJIeAXEH+N1Yw+Z+H1uo8tNflo7uhEP3NJRhsKcVYWzkmOyuwsacaWwfqsXOkEXvGmnBgohmHNrTh0ekOnFALAE5dLwCYaZQEAJtYAFCDx6aqcHp8HU6OlOL4ELsAFOM4PcvH6Vk+1isR/xIk23+J/Gfr/3U4O1YhBADnJlkAUIeLGxpwSQgAmnCVjneVjntlplWQ/5eoZNv6c9MtOL2hCScmG3B0vAGHRupwYLAau4QAoAybO0qxsbUYE42FGKrLQ29VNjrXZaG1THIBaCrJQGMpIwsNZdloLFehidAsyP9CdNaVoq+5EoNttRjrbMBUTws29rUJYn/zYBe2Dndj60gPtk30zWO0F9to2Q51uYUFASwW6G3DBnYM6Gqm+pYEAGNtdRihfQsRQHMV+psq0ddYMYceegZ6GtTkP60bpW3GW6sw0VqJqfZKbOioENH/**2**...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/408247629

---

## CASE 9: Jon Schull, EcoRestoration Alliance (7)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...Who's going, what's happening?  
  [https://www.climateweeknyc.org/event-search](https://www.climateweeknyc.org/event-search) 

![][image1]

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABw4AAAQQCAYAAAD74H+qAACAAElEQVR4Xuy9ZZvcWJquuz/uPVMMpmSwM9N2OpmZmZmZmZnJkOY0Y5qZGctU5ILugq6e7h7a51zXOXuqav7Cc9a7JEUoFGGoate05/T6cF9LHApJESnFnc+**7**/scHCxZDIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBD8ffM/tBMEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAsHfH0IcCgQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCIQ4FAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFA8HeH+RILgUAgEPwGmHHMsWSxORYvMsPCRUvw4cIlRt/DrytCHAoEAoFAIBAIBAKBQCAQCAQCwd8Z2h+6BQKBQPDbQSJx0SIzLPhvIBCFOBQIBAKBQCAQCAQCgUAgEAgEgr8zlB+zu//UKBAIBIJXSPs3tWh8UoGio9lImoiFX643rO2sDQTihwuNv5dfF4Q4FAgEAoFAIBAIBAKBQCAQCASCvzOEOBQIBIL/OsrO5iGiOQR2jnb8u3fxYvPXNn34ysWhh6cXauursW37Bty4cQ5//ONT/PzzvzyHf8XPPz0DNu+nF8DX127DxHKvhJ/+hfOzzE8//vNz+fE//vLSaNd9tdD2X8zPP/3zy2F0Dl8dRsf8FaF9nZfDxLVlxL/9Jvz086tDu2092vfyKzFxvF8Vxufk9eYn4j+fzY8//7MhP/0F/8H4Pz/+2YD/9z/+ZMCff3cBf/76LP701WnOP315Cn/8wpgfGN8/PYXP7x9AWXE4KsviGInIz4xGSnwIYsL9EB3mjwhGSKg/QlkbGxuC2JggREcHIYq1EZEBiIgORHxCKNLSIpCeFo6qoiTs2tiNHYyi7HD0NRVhurMcE91VyGHbjk8IRmFBEooLkrFrfT9uHF2Hme5a7Fk9iKgAV8SEeSHUxxWh3q4I9lqFIM9ViAn2QVp0CFKighAf5oe4UF9EBHoi1M8VgV7O8HN3go+bI3xZ6++9ElEhnshIDEFkgDt8V9rDe7ktvBxtWGsHn5VL4e/qyLa9AsEeTpwg3jog3NsJoe7LEOHpiCjvZYjxXopYNi3OZzlifZwQ6bkM4e7WCHK1hLvjAqxa...
- **2025-06-25:** ...PDDo1u37gAlf1hxlfhbFp/**7**/rof/N3+q+1TkvvCwu8TPD989GN1TYWfv1dpWaGHiyMZ6EdXCwQAlgERB6Slrqygp6Uu7tYCPxIwyE+lsEg4PB6NAXIST/NsSCJTCESwoqakrCQnr7hJTkVBEayrKioBZoFtxCUxDQhYcOFXV5JTlVunIb9eR+lLO4ZJvL9rVohvZoB7YZhvQaDnFk+H4pWaWABYJeG+JdEBpbFBAFibA10j3a3cuEY2ZgQuRZ9F1KFjALCUgHtAkBQ3UZQVzdRVeGg9JwOCu4mBB5XoQsZ6UYnuFJwTEeuAR9vjMDYYtKU+kq2tw0PqMXU0GJpqgFx8HS0hSteNhBeZUTOc7bZ6O5cEeZWG+RaH+eQGeaR52UQ7cD0sKNYUFA1gTlPRREvFVE/dXF+LhtQWUPB2ZgYiS066n3tFfMiOtOi65Ijq2MCSYLfSILdiuPvKHcCxJCZwa4QoNcjHFKOjJf+ljrKcuvxGXQ1VeD4idVVtrZW89T8A65OxwCvgdXFhd3HyOzxPDgoJzmhaKipILS0DPN6EQgHAsjChonW11BTlALDES0sOo6I4P9DXk25KZZmbpyUkjA0M+Li5mRga7N1Tf+/2rcrSEgoBT8JhAbBsbazHRoertlUQ8FgMGgluqzgczoULF16/fv1ePGiw9HblkZSViirv3n9YevvVyVNebu50M/PNqWnXvrsq3s0+dT//9xoiFAOrceIOANYX5rslzZohiw6I3vavgeU4CTkehOznpe3m1jjMf2Y/v9b+wFrnuTU+85LBR6WTzqwuurqu/r5c71OVqUUALLl9i5uml5SmP6gOv1NoebZ+2w9fZH2zOuyktPt+iD8CMQcgk16I2gUZdMBB6VopjtUFUXsg417IrB+iD0G8KQnbg5LORz4L/npd/Hdy+feVd/2m3LMkP/Z+3fSHzyffKU8ta44ua/Z8UNn15sushwi/6xD3CmR4GcJcXYW6vRr1wyrMXUnCTcjgGmT8DWR+DjI/BLFGIasOWdcditFFxOJM5p4wfqczt5PG6aOyhkzNh/iUAU90X6R2d5Zy5zalvkHFoRMAWF8OP1wDgDX6WnoFWIjRnxDDD6QGfpXpey7b9xFYXb/Idjz8vP2H34G1u1/YsDu+rbS6O6mn23Wih7YCLExXj1lTv0txW5R31WZ8wTaN4iH1gmMqOVc2pV7/POJbWb9TUq6HpISTkqwRSeoIgjgijR+VIQ5LE/qk8d0yaDhHTdyJJYVtk8Q0g0Bgm+DA1Etg6iSxlVL4Yhliriwhcw0+RJViTWUxVoDlOd3idWAv/1gL83Aj60CjfWeVW2qMA9XYUE7HYj3aXVLHT1qc5P4/C1j/4h/xx/b+A1yvcnHpw8tXi49//e3eDw+uf3/722++**7**+3tr63dER...
- **2025-05-28:** ...QEeD/kgEgZcAA8C9E/**7**+I/382ARQlniFY+v8LyI71Q1TgcQSdP4prl88hNCAAYcE3EBIc/i8MAJFc/PcPDOcC/+XLIbhwIRh+fswAEMBLxqVL1/6SAeC9AeBaNEK4+B+DG2HRuBkaiajrkYi7GUnPLjMARCInKRJFt6NQmRuDuqI4NJYnoqWaGQBYBoBb6GrMQG/LHTzszMejnkI86SvGswel+Pp+CV48KMHLh6V49agcr1lmgKfV+ObrOgEv6vHtq0Z8+7oF37xtw3fv2vG373rw03d9+OFdF+1r4waArtZCdDbn435nKR52V+BxTy03ALx82Io3Tzq4CeA18fR+I3raq9DRXIbmu8WorypCbVkhKkuKUFZUgpKCUhTklyMvl6X/r0QuUZhfhfLSOtytvIvSzCwkB/vj5slDCNrnjYtem3HRzQYXXazg52gBv03m8LM3x0UHS1xytMYlJxtccbZBoCuLmrdH2JbN9J52ROwuNyTRezjtwBak7HVFym6n9wYABov+j+XivyUiPC0R7mGJG26WuOa8AYEOZri40QTnbVbjjOUqnFi/nDDiwj8X/y1X45zNWlyme7niYIFLVF5iYj9xcdMGgfBPXKH7vcoi+12sCRv4O1vTOvUzqAxgKf7d7RDsQffdL/wLsEOopy3BDABW7w0AjGD3DQhwNafzzfhUAMwEcG7jGm4AOMNS/1ut4gYAH/PlOLJ+GQ7RfbMsAIc3sCkAjHCARfKbsSkBVuIwi+i3WI2D5qto+0rspe27TZdix9pF8F4zH1tXz+PlTtMl2GthhC+p3r3Wa7DL2gQnvJ2RFOyHe/kp6K7LRfe9HPRwA0AOHrVl41lXHl7cL8DrR9RXe1KEb54yCvDmUQ6RhTePbxPptO029e9YmYZ3T1I43319C9/Ttm+fUvkknfPd41v4lnj3KB1vHt7Gq4dZVH8Otb8CPOkuwcOucjxghpRHLfjp+xf44zfWqxKo/kz8HzAAfPv9D6itr0dhaRnyisuQXVCCjBwmguciJS0DyUmpSI6LR1JUOFIiwpDCswD4IN5vB+J83ZDg64Rk303cAJBwaiPiT9sj+qQtYs84ICtkF0rjj6Ms+Uy/AcCXC/8FKYJof04yE/8/GABymNko7Qry04NRmHET+ZlRyMuKRd6deORmCWBmgAFYFoCCvFRuAiguvC0wARR9MAFUVhSguroYdbWlvKyqpGevpgw11aX0nGUg/XYSysoL0NbegPb2etTVlSHrThpi4yMQHn0TkdHhiE+IRlpqPFKTY5GSEIXY8BBcu3IWV8/Ru/DSCUSF+CHuxlXE3wzEbWYCyEhBaXY6ynJucz7V4v+**7**+LcMAFNnyxNy3ACgqa8AbZYBgKfqnyyAp/**7**/YABgor/+cg3MXq7ebwBQxvT5kzBtniIvZyxUwkxmAOD7VKCzYDIMVkzFHCNN6C1R43Vwk8ASZaqDmQSUedT...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577

---

## CASE 10: Josean's iPhone

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-08-16:** ...Thank you all, I will leave at 5pm, wonderful to experience ERA in action with so many amazing and committed people\!  
17:00:49 From Natalie **iPhone** To Everyone:  
	Nataliemariafleming@gmail.com  
17:01:53 From Katrina Jeffries REDES, Senegal To Everyone:  
	Thank you all for your passion and information.  
17:02:21 From Jon Schull, EcoRestoration Alliance To Everyone...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/242890812

---

## CASE 11: Josean's iPhone (11)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...M7dmOkuxeToweQn5aLMP9oTI4M4fyhEfjS9xfmF4aTQ/twevQgvV4s6otLcefcFB5fPo/LYwdw5chBIRAf36BB8A06rm9cw+s7t0QS8dLoMF6eP41Le3fgzPYO3D8wRNfIJjykTvOl7dtwsbsdk+2NdC2twtG6MoxVFeJwdRH25Kdjd24GduXztbQYO6gT2Z+ZiKHCLGxPi0NXUhS2JIRjS2IIOuOD0JUcjt7MaAwWJGF3SRqRLqTh7spcDNXSa3Y14vTubsGR7U1i/UBbNY5TX+BoTyeC7Szha2UMGxo46iyeD90li2G4ei181luhjFNcocFYT79ViJsL9ndtxtWjB5AeHkKf8wZunZ1AeWoa7l2cQicNIHZtacPts2dQnZeHACdHmKtzolBdYCVkIbWcMpSJQysa5KpKw/WMlryVyUMawNrQgNWGBqwbWRyyJJTJQ5Ew5FZVHOrqSoj0oapYlAnHaSlDuUCkxwxl8xxyuVIaZLpYGNI9iY5jcwPEBngjPSYS2fHRMF4hlSSVUoeSPJTE4QIhDlka8vyGBis+hs6aeRjob0ZubiT6++swMFAnxOG5M4MCIQ/lslCG2MbicGoPLnHZUhnyOQ9ZGkriUC4TpbKl0jZJNF6n/tbYSCPu3eQ5CEfpOslzS+/HnaucHJSJw6kBXOC04WmlNDwzsR2njndh/FAr9u+tw1Xa78blXbjNz7u2V8YQXWeHcfc6t8xeuvbuEzy4sVcIxAc3RwRBfu4KVOc1FNIwQCpRGh7irUgZSnMbyqWhH6IjZkvDuJhQgVwaJgppKKUNWRxOTxvKxWEiMjOk+Q05aZidRWRL4jA3J32OEqWcNlSKQy5TKheGgupyWeJwhjhsakADS8PmJjRtbkZz62ZsbpPNb9jZgXZOG8rLlLI47NmOrl5JGgpx2CfNb6gqD1XF4eDQMHYPj8wSh8cnp3D63EVMXb6Gi9du4vLNO7h2575IHTJcqpTnO7z3mFOHb/DslUwYvv8a77/8Fd598Q1te4frt+5h9NBRev/tSE3Php9/CGztnGBobA4NLT2sU9eGmoY2tLT1oEfXckMug2lsCmMjGUIWmsCQrv2GnD7k+QtFSVI9GGjrQl9LF7qaOtCl12DkwlBXTQs66zShu05DoC/koQYM1dRhpK4u5l3VX7WCzq0lsNNeh1injWhKisS+mgJRsnS8Lh9HqjJwrCodJ2sycLo2E2freU5DTvrl4lIzJw05ZZiH68QtmTS8v6UYD+XScFsZnm8vx8u+Srzur8Kb/mq8GajB2x21eDvAspCW+2rwOfGurxbv6Hx+**11**+Pz4m3ffV43VOL593VeMTisLUI15rzcEUmDi+KxGGuEJmTDTkYK+P5wuOwOz8OO/Pj0ZuXiM6seFTFhSDZywneViawVF8LQxqLGamtg7GGBow0NWGkrQMjHV36PiUMCH2BjmgNhECUhCFLRF5ncSiEokweCpFIj/OchmJeQ95X35DGidPhxCGnEyW5yGVMebv0fH1OIdLf1NPRpr+hQ7+5PixMTWBrvQFuLk4I9PelczWSzj0ua8oJwSJUlBajjM6lovxc5GSlITONzsd0hs7NtARkcDlhOl8FqTwnqURWejyy0xOQQ/dAVfKy6LWzU6gfkIqi3DQUM3n8P9EzUCaTiUqyZNuyJMHI8HoBbaf9S3PTUZyThiK6HhTReytUKTuaT++TyUvh0qMyUZgYi8z4GCEJWRCmxkQgNTpciMKUqHAkRYYRIYgPD0ZcWBBiwwIFLATjaBtvj48IFstiPULaJj3O+yvFYRSLQx6DB/og1N8bwX6eCPRxE/Md+rg7SvLQ1R5eLvZCIHo6sUSU+KHi8D87Qmyq8Ht6738K3yoOf/0Kv/vNa+LPnzqcLQ6lOQ5ZHHK50n+i5f/+2zf4v373Hn949wh3J8ewt70GHUXpaM1NQiuLw/RYNKVECXnYQm0bz3eYES9Shzv5P5XVlOBAbZlgqLwA/fmZ2Eb9xs6UeGymY7Q6NBDFvjS+8HBBrrszCrzdaHzsimw6dtIdNwppmOW8icbQHmiLj0IfnQe7CrMxXJqPQzVlOLm5Dheov3p7d78oU/rm2EG8mziC96fG8X7iML46cwxfTo7j8xMH8fwQ9Qn29uNq/xac3dKIY00VOFRdiH1l2dhTlIHdPDd3AZcklctDloYSAyJpyMKQS7HKSRKlWfmz9uSlYYdMHO6gz7mjsgiD1Hfe116PI31b8OTSJP7tm3f4n//6j/jX3/1SzF/4zfvn+PUXLxUJQ5aG//g1nQs836EQh68E0...
- **2025-05-28:** ...GAFp3ZUcH6PlPa/nisjjbw43syrU628MdfBzcNS6v8e3jvZy/sn+/hAGvV/eoBPBJ9KnOrnU1H/yfEePpanAGjno8OtfHiomQ/mpLT92xcMAJXcHinn1kiFwgDwDfFfYQCoWDQAyKn/p+t5f1Yh/v8zA8CHc62yCeC96SbemWrkzmQDtybq5CwAN8breF0yAQxX8+L+BRPA4FbO9hVxpmcTp7oLOdFVwHFpXvGOAg5JWQFacplpzmWyKYeJRgXjC0jLU025TLfkM9tawJxESwEHWzdxuL2I+Y4tHOlcEP67SzjVu43n+ss5O1jF+R01XNi5nQu76ri4p4GLexu5uK+Ji/sVXNrfzOXh1gXaFmjnymgnV8Y6uTrexdWJbkEPL0z1cW16gGszQ7w8O8SrB3fz2iEpff9+3pg/oBD8j43y9onxRW6emuDW6UluCqTy9nNT3BHlXcE7z0lMcO/MBHdFefPUuGwSuHv+IPcuHePwzg7ivR2x1lDGTlcdJ2N97Az1MNPWxEhDHSsdbaK9PdjZUMuHL16Ed2/C3TfhzRcFV+HmCwoDgCT+S+svX+CrF8/z1bXn4VWx/qaUGUAabX8L3rkjlt+GG2L/**11**/jL1ev8psz58R9dYy7k9Pc2D/Kazv3cK1/kKtdvVzt7OZKexeXWtt4vqmZFzo6ubFrN++PjfPZ3By/O3aMP55SmAD+ev45vrpyHl65Ir7LqwtTAdyVMwEsZgF41ADwznVF5oI3rvDXy6f4aG6U13f2cLmzifOt9Zyqr+FEXQ3Pd3Xw5vABPjh6hM9OP8fvLl3h79eltP63+fKV69w5fIyLQ3s41trFXF0zu4uKaU5OozkllT7xXt1fUspEZSWTVVXMVFdxaHs18+JaHtpezomWWi4NtPPm6E7enRvhzvRebk/t5ubUDt6e2smNyZ1cH9/JKweGuLqvjyv7erlyoI9zO9vZvS2PfD97Eux1aUj151hXibgvt4p7fjOnu8T9L+77E+0P0//LBoC2PE7J5CoyAXTkcqbzgfi/kQs9kvhfIKMQ/xUj/f8x9b9kANgi1iUTQBFXBjdzsa/gH6YAkDjekrYwDcBDA8ChesXo/9mGNOaaMjj0iAHgqGQA6FMYAE7vqebMgTrZAHBhXDIAiGfkYP9DA8DZrxsA3r9xho9uPTAAvMyvPr7Obz5762sGgG9OASCJ/3/569fF/0cNAN8U9v+7fFP4XzQA7GxG2XgVKqZrZOFe1XItOo5q2IeY4xHngG2QkehHq2Luo419qIk8HYBkADDz1kJfSi3tKOIJ/Z/xpMoP+InKEzyrKY1MXY6K2WrWmqzgpxv+g3UWK7GPsMA+3BwzP13UbVaiZPwzcd6foW61BGs/TdyiTHCJMMY92hyHUH1Z9JdwjjLALlgHY4/1smlgg8VS1KxWiv6...
- **2025-04-30:** ...Unable to turn on the speaker on my computer

	

09:**11**:08 From Jon Schull, EcoRestoration Alliance to Everyone:

	https://docs.google.com/document/d/1YIuNweYopFKxFHbfDkaGrhvQcxn\_dmActdsyUrEnMSc/edit?tab=t.0

	

09:**11**:00 From Edib to Everyone:

	Sorry and hello

	

09:**11**:17 From Jon Schull, EcoRestoration Alliance to Everyone:

	Activities and Projects in the last year.

	

09:**11**...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/242890812

---

## CASE 12: Joseph Manning

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/85761700

---

## CASE 13: Joshua Konkankoh

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 2 meeting(s)
- **2024-05-22:** ...Olowosile, Alex Carlin, David Ross, Aude Péronne, Cindy Eiritz, Edib Korkut, **Joshua Konkankoh**, Laura Pérez-Arce, Roberto “Beto” Pedraza Ruiz, Anastassia Makarieva, Rob Lewis, Nick Catranis, Folorunsho Dayo Oluwafemi, Grant Holton, Michael Mayer, Pati Ruiz, Nathalie Ríos, Jake Kelley, Marius Iragi

## **Agenda** 

Updates and introduction

* Sanmi Olowosile , **Joshua Konkankoh**, and Cory Albers \- [Source 2 Source – Think Like Water](https://source2source...
- **2024-03-14:** ...Solar albedo reduction in cities.  
* **Joshua Konkankoh**, Cameroonian Environmental Journalist and activist. Background in social security. “Permaculture the African Way.”    
* Kethia S. REDES, Senegal.  Working in Northern communities fo Senegal and Maurtitania  
* Philip Bogdonoff, Bio4Climate  
* Eston Mgala, Malawi, permaculture agroecology and Regen ag.  Country director for Permaculture network in Malawi and African Union.

How can we work together??

* [Africa, ERA...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/99648620, https://fathom.video/calls/76758727

---

## CASE 14: Joshua Laizer

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577, https://fathom.video/calls/285134478, https://fathom.video/calls/242890812, https://fathom.video/calls/223525279, https://fathom.video/calls/214375292

---

## CASE 15: Joshua Laizer (4)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...yBeqUZx9SqUkPJLG6CpWI7S6pUIjUrGhClzMXLMZNg5uiMmIQUJCgaHuZCrCiDLKEBcihqpeZXQ1K1FWeN6VK7YjMrlm1HRuBHlDew63CxqHBY3bCZ9DZm6AYtD0uEenUNjTCWNKXVIyF+O5OI1CFaUw9YzCabWAZjrGA5L11jYeyvgFpYNv3gNAmVlCJZXIEhRSeNVBfxJfrJy+MkZHvI8g8My+CfxduUIk5chKKEQ7iGpcPZNgK1bJOY7BmK2tTdm23jC0tkfzt6R8AlXIFKuRkJqEeQZ1O+yGSAymFuG/OI6AQ8LS2pRWFwjiec11SjiiNCiKiENqVhDraYSRXR/lRRLbRHdb6Ul1Sgrq0VpWQ1KSmtQWl6HkrI6FBVXo4C2z80rJZUIMJlDbba6FFlCZcL5mEltFl1jBoZZpJzCGsltWFIHTelSlFY0oLK6EdU1TaRGLFu6Ak0Nq7CiYSXWLF+NTV+sx/YNm7F/604c2bUPp/e34mLrUdzgmobsMjx9AQ/PXBQuQ9YT4Ta8jG8uckyptrYhg8ObDA4ZxjHAY3DIgLCDo1AAwnaY+Dw47Og6ZFD4VFsL8dsO0tVEbAeI7VGlWnDIQFDUNtRKLOtc45DjVDlWlZ2GnRyHN/n73KDvdg1Pr1zBk8tX8OjyJTy4dBF3zp8jnceN06dw8cgRnKb3sxP79uHwrp3Y9sVarKyqQEVuNmoL8tBQXISm8hI0lhejvkyDqoLc/**4**+99wCr6krb/mcyedMmySSZZNLrpNhjiV1RsCCCgAqIgCIKiPTee++9994RQcQOFrD3gl1U7F2jUZPo/X+etc85HFBn8n+/+d6Z97sy19xZu519ztln77XX5ud9PyjLYddhOiryuNZhJioYHObJwWEGyjmOqDCL2ixUysBhNe2norCAlC/m68qLUF+Rj6WlOagrzUR9WQYpHcuoXVaWjYYyCRwuryxAI2l5dTEaqzmutFzUOlzTUIm1jdVoaZbiSjeurkf72gaF23Bv21oc2Noiokq5xuFRWVzpsb2bcWIfx5ZuFQCRY0u5ZYDI4JBhIev+jbMCIN68eAw3L53A7SsnaXknLT+DB7e6BER8ePsCSQKHD+9I4PDX+zfo95S5Dh/eVESW9gSHXOvw31fnsPcfsn/Xf4bSY9OQFpuKlOgUJEYkID40DnGhNAYIjkF0UDQiAyKEogOjEMfgkBTpG4Zwz2AkBsagLKUAZYl5yA9PQ2FoGkrCMpHqEokkhxBku8cgxyMO6S5RSHOiZfahSLALpvVR8Dd1QXZACvUjP+P+lYe4eJnB4X2cuk2684Dan9B1/zHO3PkZB85ex5rth1CybA1qmltR17QOZVXLUFe3AiuWr0VV5TJkZxYiKTYFqVGJKKL7aFFaNkqz8lGeU4iSjDyaz0FOQiqC3LyxoqYBD2/+hLvX7uEW6eKFW7hM7c17v+DK7V9w8ebPOH/9IbquPkTn+Qc4evoOjpy8hSOnb+PwqVs4dOomDp2mtvMmOs7ewvEL93CavkPntUc4Re3ek1ex//R1HO66LdRx/g4O0nb7GRqyzt6klkTLDp6/S/oRBxggcozp2TvYfe5H7Oq6h10X7mLXpVtoPd2JlScOIn5lBVwKY+BdnYSAxjQErEgVUaXBa6SYUlZ4S6ak1kwBDSNasxTgMGZDHhI3F6P0yEpR51CAw7sMDjuw6W6HqG+**4**+c4RbL59FG0kbsW0kttQGRxK0PB3cPi/QQwKWXFB7ojyd0Y0iZ2F6VH+yI4PERAxys8Z4T4MBZ0Q4e2IEA87hcsw3NsJYZ6OivkwLydE+boi2s8NMQEetD93aj0FEIj2o/fg+EAvFwENQxgUejiL6MJwTwnuhTNE9HBEqLujBA6fAw0FOLRjQChFkIrah862AiTyMq6RyPuJoPeK9nFDlLergJLyfXEpHd63gIYMJx1tRFQpA0MPywXwtlqoAIcMdRgcuiycqwCHvtZmCHFagjAXWwTYWgrYYzFLS8SU6o4bCZ2xIzB/+hR4MQCyXghPep2jiR5sOAqUXX0zp8FMgMPJEjhkh99MDVjpa8F2ri4cjGeL7RkcMozzX7JQQEAhmevQ38pMch4yxBQ1EBcjgl2HDA+5LJCoa2ghtuuGhgzD5sLNlGM46TvN0xdOQ4e5s2CtPwPm2lNhpjkJCzUnU8tgkF2FEjgU8HD6ZFhwVCmDRQEO1TBv6kSYTZ+EJbO1BJRMpd+9PiuJlCzAYZg9g8NZAhra6+tItQ3pmApo6GaLrEAPAQyrkyJRnxaH5rw0rCvOxqbKQmyrK8Oe5TU4tLoRJzesRtfWjbi4s43Ujgukrh3tOCvAYRs6ad2xjetwcG2zgIc7GusEONxYVYrWimLR8jwDxK311dhQWSJiTMsTIpBBnyHaZYmITWVw6G1uLDkOZU5MCRyy21ACh8I9SN+fIaACHHIEqQ5rqtjObs4MmVtRRyzjWFNTTTXpNbocS6sJW8OZcF4wFx7m8+ncmi8gtIi4pfMuhH7DeF8PpAT5ITUkAGkhgUgPC0JGeIiAh1mRYcKBmB0dLuoacjJHSUqiBA97iV2H+QkMDmMEOEyPCJdBw2AFPEwJCRL1DeP9/QQ0ZIDI0JAdh0m0LjU8VMSSsruQIWFmDNchjBBuxLTIcLGclREVTvOhtD2NBUL8ER8kQUMGiFzvkGEg9wMMC53oO7Pr0I/PV28X8Y8KGCwyPOSaqAwQk0L9kBQWIJTIoDe4Z23DUOo...
- **2025-06-25:** ...y7kfL9m5sPP+kfbb+9dvn1c0e1qkb/PVLzYFLs+rCNnOBovPBZeXVm1asGGe2TW1+3rlla+3lxx5q2D+G/tOLL76xanemweXrbXkM+N3H7Nc+qzk+jcl9ZEZ1c3Ly717TrfVbGxsnjB9S7p15cvLtq1q9tbc6DkW8L/BrX6ePjSCrdXy3iQe9lhMt4ZH0G2pNMSPxDFVdFqIgBVn6wYzUPG/rOQnfgQBYNVTNFIj+MJpPwEs2Ml7Up0ityHT4h7J1I8wlGVM3p89Zc9oQ2nGlJ0Z03YhZebuzsrbg4RmgEjkGAmdF5U1bfeI3F1IOdN2EqHjkXm7pRqVv0fUaMNeUY8Z94l63FT6hHn/GMsBqcZaD8YEx0/SSIdI+xRzSDyOa9G/nmIPyFt4ALNf3sID2FJ4ALMPTuJ2LL13LF0qbx9nDuTQB0fYjj/mPDHSdjiTLk2zlmaxx0bZy7PZKkSH6VZ3qsUDBf8gjQyWPUp7QpwXE0kELJGx4oez4fSjAVYcY31vwCIi5ljPYsBiESu0EakxYCHwTIN92psyOW+qvS2nIIS+zVfm7N3c0L7qjGfKkgPjHbtG2o6mOcpVBdXKglqVq1bnQLjdkMM2wfhUgJ5Y85jzfA696xdLDy5vDM4sO/vCrKVPF20azR9PZxpUfCTJ1UEVR6jikNopGTxiZTwGUcsI/uzrMzeuqz5afu9U469OVt84HvnC7b1ed6bz3NwjGz5ePvdV1/SF+**4**+5r/TV93bSi9dPnFrwgqHodcZhnuc419ns/vrbVd7LLyw+o56yaO6hg9WXwzVXLs/YV/usvWoMU/bqjDUn22tarhzourm/**4**+7ZS9/1+O9dO33xnr205QnHsQy2Qs82wZJjofAS+hpFRyAoziP1vQFLSle/h4AlXAq/Fr4lICaCFYoJMxYN4cIkpi7FVkOxZyjmjIar0NPladOOPzZl/4v529/KW5pLzzLbuXxb7hRX3kfT2beKCl6wFY9nFoycsjT9vU3ZU0+OMrZkGENo6EpGVtJ+lrKfoOzHKNupFLpKbfakGtpSjR1aK0wMhgYs8TywFA7sErqKhQjDBLBSHR066GaNI+3nH7cfH8Pvfrlw1qZzto7Plrm7F83dyL7tWP0Ku9L8CRf6bH/fr9avP/6yZeaT9f5F33w1/2r3x9Gw4bP7qxoaTFdvze28llfle/bzX03vuzU7tzizaOUzfReZX3/tvHohrzVk7e3eVucrm7X7zPiiQyPtVZl2b6bN/xCABfvyxu7cYfST9WDhPZshAUthaQLAIlUV6DBlgpJsatartVbnMGdfnVtv2Riaud2z7UhtXVOwwRN0+yN1ntbS43Xz1x37yLXjFf5QTu7hTGOtclqTIjegNLdTUwNqayfk/xnbVCZYaZFijqSYhb2cVaZmJFxJBO7BJAtUZ0Bgh7dGDqmsUY0liib3etajsdUq7bVKp1dhCyu5Xr2tD41Jo23nx/I7Ppyz/Fzj0Y4LlVVdTQsOHHmJXv0mu2z7yW2+niPtN8sP1h153bZm9NTV4yzzFx087W7vCfTeNC3e+5xlzQvWtTO2naq7Gqm/5F+562jxJ+sqw2dDNys6Pqvo...
- **2025-05-28:** ...hy7cBylM/xqRzsL9ERviy3SpQJCHMzwdrOFOnHrYmcLLngVTBzME2JvB35YFZ/**4**/KjtDxLtZIj3ADkXhLmjODMLt4kiMX9Nhti0bm/3l2Butwf5ELbZnq7ExXYH5iSJMTRBMk5kSqkbnsrCwXUKUisnia49XOHpYhlXic+mwFIsParD4qB6LT64yGrD8f8Tiw/rjARv71ZjZr8L4ZgmG1wi2lTwMLGZjcDEHk+slmNupxObja9glSg9f3yRKe/BCoPSvI3j3yyhe/zyMVz8O4sUPA3j27h6evr2Lx2Lqp5e3cPS8DQdE6T5RKkAqNdM/rCUuqySILhDU81uE71YeZrdzMbeXh4WDPCweEdYHhMBeJlGcKsF05TAHa0eE6RGxfpCDlZ1MCaRiPfaljVyiMx+Lq0T7ZAomCZ7NbTEfZR23VVjZIHxXSjE5e3zs+kZSMDiewffz3Fsi9pcI9cUyTC0Q6/OlGJ8TEC3hZ5dKMTJZiIFRovROKjq6NARpNK5dD0NtbRDy8tyQonMgFPTh5SFAehrODqdhZ/Md89LPoHfpU1y6+DkML38HU+NzfOw09C99ROnprwjSLyWUnvj2U3z31Z+I0D/gm8/+U4pvP/+9FKe//TP0zn4NcxZu7Cz0YGN6AaZ6J2BpeBLermYIdLeEGws4VvpfwuLiZ3Ay/wb+zucQ42+MEp0brhUEo7s+FnevxqG3hhitCkF3hRK3ivzQkueFq8TI9UwFbhb7oasiEF2Vgbhd5Y97DUpMdsRg5nY85u+qsUigLg8RnkTq0rAGO0wn99eLcH+zGAdMOzvL2VhfyMTGIoG1qCNSNVicUmN+MhFzjNmpRMxMEqWTqZibSsfMNAE2XUiEiprSKwymy4XrhGkj5uabML/YTIyyEL7aidW129je6sXh/l28fDqINy/u4d3r23j75ireEKWv3qTj9Rsd3r3X4P0HHT78IG4LmKby8VQ8f6XDwYN4bO5GYnFdxf/YDyMzPhicJp6mA3B3wh+9Y/64PeKPrpEg9EyoMLwch4mNZMwfZvAcScXkro4gTcLwphrd8yG4OemP5hFPNPQ5o6HfGY0jxzC9OU2UzrrxNR7omnUnXhUEqQvaxp2JUjfcXfLB0HoQ5o6isPIoAZvP0rD1NIsozcfSbi6mljNwsycO9Y2hSEmXIzqW+aOfMXy8jeDvK8bIOCI2UoEMbSAKssLQUK5Gc40G7bU6ojQRbRUJaC+NRXtJNNoLwtCWEyw14d9IcUczUdqcTJAmOUkoFU34rSnH00S1pbmgg+lATBHVV0iUMn2MlgZiplqJ+Y8gXfkXSkOkWL8ahq3GCGw1RWGjUdSShmKuOlgaIDVAhwzx/Jgq8/s3kEooLSRksgqsCSbiSSMmjDeGDZGpZ/A9Lhl8J4HU1OgMzEzOwtLiPGytL8HJngh10IPcxQAKOUNxWao+9vY15kXbSJr2ydLmnNS/1NzqAlF6HsYm52BsfJawPQs7foazox7c3PUIvEuI0RkgNs0EkYnmiI+3RVKiHbQaGRJFc3yiDCEhApbGiNEYIzHNgmGG5EwzpHG/i+qcUXLFBYW1TsivdERGkahJtUF2ESFXaANdrhUhayM1+Wfmygg6J5RUETAxFlCxxKjREJwZ1kjOspQ+W5NlhexyFxRUuyK7zgWpZfbQ8bOyyh2Rz8cyS+T8TCIwwxWJ6S7EvANxacXjZgZ7VzEIyYgZmQk8fUzg7kOgqsyJTGskaMTSnQqGGyLjCbBIe2lVKNGErwyxRlikHcKj7aTXhkRZQsUQtZfJYtBVsZz744GsEi/i1B26bBfoiGhdLkGZ5YCYFKIt3gwqtSmi080Rm2rM11kjjcchrcBOwnt5jQK5Je7QiKakWBkzazHLgQXSdPZIJppDE80Qq7XAtStMtO15KK9IQXxsAGIivKGNP55HNFw0nfsrpBrNYKJPRQBGhRw3vx9D1E+a0kk0rYtm9uOaT2dpsJJ4LIKACCUSg31cP2LSiQAlLr1Ezai47SiFP4ERwAgiAoK8nKRtgLs9gWoPH7kdvFxs4elsA4WDJeQMN0crKeS2FnC1MYeDuRFkZoawZ0hb3rc1uQwbY30p7EwNYGdGoFkawdHKGK4yC77fGp6uAsH8Pk+e8CF+Esh0SRHISotDUa4GV6vz0HqtFIN3mjA90sGLaz92iMUHe9N483QVb5+tEWr7+Nt7YvSnh1L89uMD4lWAVdSY8nGx5fN/**4**+t+frWDN09W8eJoHs92ZnF/ZQyDnQ1orMlBRUEyyos0uFafh...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577

---

## CASE 16: Joshua Laizer (7)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...Who's going, what's happening?  
  [https://www.climateweeknyc.org/event-search](https://www.climateweeknyc.org/event-search) 

![][image1]

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABw4AAAQQCAYAAAD74H+qAACAAElEQVR4Xuy9ZZvcWJquuz/uPVMMpmSwM9N2OpmZmZmZmZnJkOY0Y5qZGctU5ILugq6e7h7a51zXOXuqav7Cc9a7JEUoFGGoate05/T6cF9LHApJESnFnc+**7**/scHCxZDIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBD8ffM/tBMEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAsHfH0IcCgQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCIQ4FAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBYIEQhwKBQCAQCAQCgUAgEAgEAoFA8HeH+RILgUAgEPwGmHHMsWSxORYvMsPCRUvw4cIlRt/DrytCHAoEAoFAIBAIBAKBQCAQCAQCwd8Z2h+6BQKBQPDbQSJx0SIzLPhvIBCFOBQIBAKBQCAQCAQCgUAgEAgEgr8zlB+zu//UKBAIBIJXSPs3tWh8UoGio9lImoiFX643rO2sDQTihwuNv5dfF4Q4FAgEAoFAIBAIBAKBQCAQCASCvzOEOBQIBIL/OsrO5iGiOQR2jnb8u3fxYvPXNn34ysWhh6cXauursW37Bty4cQ5//ONT/PzzvzyHf8XPPz0DNu+nF8DX127DxHKvhJ/+hfOzzE8//vNz+fE//vLSaNd9tdD2X8zPP/3zy2F0Dl8dRsf8FaF9nZfDxLVlxL/9Jvz086tDu2092vfyKzFxvF8Vxufk9eYn4j+fzY8//7MhP/0F/8H4Pz/+2YD/9z/+ZMCff3cBf/76LP701WnOP315Cn/8wpgfGN8/PYXP7x9AWXE4KsviGInIz4xGSnwIYsL9EB3mjwhGSKg/QlkbGxuC2JggREcHIYq1EZEBiIgORHxCKNLSIpCeFo6qoiTs2tiNHYyi7HD0NRVhurMcE91VyGHbjk8IRmFBEooLkrFrfT9uHF2Hme5a7Fk9iKgAV8SEeSHUxxWh3q4I9lqFIM9ViAn2QVp0CFKighAf5oe4UF9EBHoi1M8VgV7O8HN3go+bI3xZ6++9ElEhnshIDEFkgDt8V9rDe7ktvBxtWGsHn5VL4e/qyLa9AsEeTpwg3jog3NsJoe7LEOHpiCjvZYjxXopYNi3OZzlifZwQ6bkM4e7WCHK1hLvjAqxa...
- **2025-06-25:** ...PDDo1u37gAlf1hxlfhbFp/**7**/rof/N3+q+1TkvvCwu8TPD989GN1TYWfv1dpWaGHiyMZ6EdXCwQAlgERB6Slrqygp6Uu7tYCPxIwyE+lsEg4PB6NAXIST/NsSCJTCESwoqakrCQnr7hJTkVBEayrKioBZoFtxCUxDQhYcOFXV5JTlVunIb9eR+lLO4ZJvL9rVohvZoB7YZhvQaDnFk+H4pWaWABYJeG+JdEBpbFBAFibA10j3a3cuEY2ZgQuRZ9F1KFjALCUgHtAkBQ3UZQVzdRVeGg9JwOCu4mBB5XoQsZ6UYnuFJwTEeuAR9vjMDYYtKU+kq2tw0PqMXU0GJpqgFx8HS0hSteNhBeZUTOc7bZ6O5cEeZWG+RaH+eQGeaR52UQ7cD0sKNYUFA1gTlPRREvFVE/dXF+LhtQWUPB2ZgYiS066n3tFfMiOtOi65Ijq2MCSYLfSILdiuPvKHcCxJCZwa4QoNcjHFKOjJf+ljrKcuvxGXQ1VeD4idVVtrZW89T8A65OxwCvgdXFhd3HyOzxPDgoJzmhaKipILS0DPN6EQgHAsjChonW11BTlALDES0sOo6I4P9DXk25KZZmbpyUkjA0M+Li5mRga7N1Tf+/2rcrSEgoBT8JhAbBsbazHRoertlUQ8FgMGgluqzgczoULF16/fv1ePGiw9HblkZSViirv3n9YevvVyVNebu50M/PNqWnXvrsq3s0+dT//9xoiFAOrceIOANYX5rslzZohiw6I3vavgeU4CTkehOznpe3m1jjMf2Y/v9b+wFrnuTU+85LBR6WTzqwuurqu/r5c71OVqUUALLl9i5uml5SmP6gOv1NoebZ+2w9fZH2zOuyktPt+iD8CMQcgk16I2gUZdMBB6VopjtUFUXsg417IrB+iD0G8KQnbg5LORz4L/npd/Hdy+feVd/2m3LMkP/Z+3fSHzyffKU8ta44ua/Z8UNn15sushwi/6xD3CmR4GcJcXYW6vRr1wyrMXUnCTcjgGmT8DWR+DjI/BLFGIasOWdcditFFxOJM5p4wfqczt5PG6aOyhkzNh/iUAU90X6R2d5Zy5zalvkHFoRMAWF8OP1wDgDX6WnoFWIjRnxDDD6QGfpXpey7b9xFYXb/Idjz8vP2H34G1u1/YsDu+rbS6O6mn23Wih7YCLExXj1lTv0txW5R31WZ8wTaN4iH1gmMqOVc2pV7/POJbWb9TUq6HpISTkqwRSeoIgjgijR+VIQ5LE/qk8d0yaDhHTdyJJYVtk8Q0g0Bgm+DA1Etg6iSxlVL4Yhliriwhcw0+RJViTWUxVoDlOd3idWAv/1gL83Aj60CjfWeVW2qMA9XYUE7HYj3aXVLHT1qc5P4/C1j/4h/xx/b+A1yvcnHpw8tXi49//e3eDw+uf3/722++**7**+3tr63dER...
- **2025-05-28:** ...QEeD/kgEgZcAA8C9E/**7**+I/382ARQlniFY+v8LyI71Q1TgcQSdP4prl88hNCAAYcE3EBIc/i8MAJFc/PcPDOcC/+XLIbhwIRh+fswAEMBLxqVL1/6SAeC9AeBaNEK4+B+DG2HRuBkaiajrkYi7GUnPLjMARCInKRJFt6NQmRuDuqI4NJYnoqWaGQBYBoBb6GrMQG/LHTzszMejnkI86SvGswel+Pp+CV48KMHLh6V49agcr1lmgKfV+ObrOgEv6vHtq0Z8+7oF37xtw3fv2vG373rw03d9+OFdF+1r4waArtZCdDbn435nKR52V+BxTy03ALx82Io3Tzq4CeA18fR+I3raq9DRXIbmu8WorypCbVkhKkuKUFZUgpKCUhTklyMvl6X/r0QuUZhfhfLSOtytvIvSzCwkB/vj5slDCNrnjYtem3HRzQYXXazg52gBv03m8LM3x0UHS1xytMYlJxtccbZBoCuLmrdH2JbN9J52ROwuNyTRezjtwBak7HVFym6n9wYABov+j+XivyUiPC0R7mGJG26WuOa8AYEOZri40QTnbVbjjOUqnFi/nDDiwj8X/y1X45zNWlyme7niYIFLVF5iYj9xcdMGgfBPXKH7vcoi+12sCRv4O1vTOvUzqAxgKf7d7RDsQffdL/wLsEOopy3BDABW7w0AjGD3DQhwNafzzfhUAMwEcG7jGm4AOMNS/1ut4gYAH/PlOLJ+GQ7RfbMsAIc3sCkAjHCARfKbsSkBVuIwi+i3WI2D5qto+0rspe27TZdix9pF8F4zH1tXz+PlTtMl2GthhC+p3r3Wa7DL2gQnvJ2RFOyHe/kp6K7LRfe9HPRwA0AOHrVl41lXHl7cL8DrR9RXe1KEb54yCvDmUQ6RhTePbxPptO029e9YmYZ3T1I43319C9/Ttm+fUvkknfPd41v4lnj3KB1vHt7Gq4dZVH8Otb8CPOkuwcOucjxghpRHLfjp+xf44zfWqxKo/kz8HzAAfPv9D6itr0dhaRnyisuQXVCCjBwmguciJS0DyUmpSI6LR1JUOFIiwpDCswD4IN5vB+J83ZDg64Rk303cAJBwaiPiT9sj+qQtYs84ICtkF0rjj6Ms+Uy/AcCXC/8FKYJof04yE/8/GABymNko7Qry04NRmHET+ZlRyMuKRd6deORmCWBmgAFYFoCCvFRuAiguvC0wARR9MAFUVhSguroYdbWlvKyqpGevpgw11aX0nGUg/XYSysoL0NbegPb2etTVlSHrThpi4yMQHn0TkdHhiE+IRlpqPFKTY5GSEIXY8BBcu3IWV8/Ru/DSCUSF+CHuxlXE3wzEbWYCyEhBaXY6ynJucz7V4v+**7**+LcMAFNnyxNy3ACgqa8AbZYBgKfqnyyAp/**7**/YABgor/+cg3MXq7ebwBQxvT5kzBtniIvZyxUwkxmAOD7VKCzYDIMVkzFHCNN6C1R43Vwk8ASZaqDmQSUedT...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577

---

## CASE 17: Joshua Price

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-03-29:** ...Where resources get scarce, their **price** goes up. We don't do that in fisheries, the **price** remains zero. And that's causing all sorts of absurd behavioral problems where as a fishery gets scarce, the incentive to exploit that fishery actually rises rather than falls. So I think there's a real problem there. And the basic market incentive...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/168082460

---

## CASE 18: Joshua Shepard

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/28854293

---

## CASE 19: Juan José Pimento

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-11-08:** ...16:23:16 From **Juan José Pimento** To Everyone:  
	Thank you everyone\! unfortunately I have to go to another meeting but I hope that this is the beginning of a long term relationship\! Regards from Panama\!  
16:23:45 From **Juan José Pimento** To Everyone:  
	Loved to meet you all and the conversations  
16:23:48 From Louise Mitchell (she...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/48059317

---

## CASE 20: Juan from Panama

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-11-08:** ...16:18:14 From **Juan from Panama** To Everyone:  
	Dear Eduardo, amazing you mention the Emberá’s. The Embera in the Panama Canal Watershed are already part of our conservation initiative on the east side of the canal and their territories are counted into the 375,000 acres of this effort.  
16:18:50 From **Juan from Panama** To Everyone...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/48059317, https://fathom.video/calls/42536046

---

## CASE 21: Judith D. Schwartz

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 2 meeting(s)
- **2025-01-08:** ...biofi.earth/about) ; [https://www.hylo.com/groups/biofi](https://www.hylo.com/groups/biofi) 

  * [Geoffrey Kwala](https://www.linkedin.com/in/gkwala/?originalSubdomain=dk) Africa, Copenhagen, Munich

  * [**Judith D. Schwartz**](https://judithschwarz.com/) and [Kyle Lawson](https://www.linkedin.com/in/kylelawson/) [Soil Centric](https://www.soilcentric.org) \- app: [https://app.soilcentric.org/](https://app.soilcentric.org/) 

  * [Zach Weiss...
- **2023-08-16:** ...Time is tight and there may be questions…  
16:18:39 From Jon Schull, EcoRestoration Alliance To **Judith D. Schwartz**(Privately):  
	So glad you’re here.  Jenny Pell just started talking.  She’s been in Maui for 40 years and does permaculture around the world  
16:18:49 From Jon Schull, EcoRestoration Alliance To **Judith D. Schwartz**(Privately):  
	(And as...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/209204233

---

## CASE 22: Judith Rosen

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/213588452

---

## CASE 23: Jules

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/220163703

---

## CASE 24: Julia

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 2 meeting(s)
- **2024-09-04:** ...Jon, Philip, Ananda, Maya, Fred, Didi Pershouse, Nkwi Flores, Amanda Joy Ravenhill, Evan Lam, Patrick Campbell, Louise Mitchell, Edib Korkut, Haley Kraczeck, **Julia** Lindley, Nima Schei, Ruth Otte, Marius (briefly), Iuri Herzfeld, Ana Calderon

## **Agenda**

* **Amanda Joy Ravenhill, Project Drawdown,**  [Museum of TMRW](https://docsend.com/view/3yn3j6anazygsw6q)   
* [**Didi Pershouse**](https://www.amazon.com/Ecology-Care-Agriculture-Microbial-Communities/dp...
- **2023-03-29:** ...I have just interviewed **Julia** Barnes about that. She's very knowledgeable and I can make that interview available to Philip and others when I have it ready in a few days. As far as population, I agree with Rob that population is set to stabilize. I don't see the problem as being population itself. It's not how...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/143656774

---

## CASE 25: Justin R-Söndergaard

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/56449118

---

## CASE 26: Justin Ritchie

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-09-13:** ...Member Updates and Introductions***

* [***Maria Ehrnström-Fuentes secured grant for ecological restoration research in Global South countries***](https://fathom.video/share/JLzRWNoRc8M5_z1o-fgw1yyPNTiqUgym?tab=summary&timestamp=600.0)  
* [*****Justin Ritchie** outlined Transition US's shift towards on-the-ground action and bioregional hubs***](https://fathom.video/share/JLzRWNoRc8M5_z1o-fgw1yyPNTiqUgym?tab=summary&timestamp=2811.0)  
* [***FarmTree presented tool for...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/37381089

---

## CASE 27: Justin Ritchie (3)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-17:** **EcoRestoration Alliance Town Hall Meeting**  
**Wednesday, 2025.09.17 **3** pm ET**

---

[**Join Zoom Meeting**](https://us06web.zoom.us/j/88139848852) | Meeting ID: 881 3984 8852 | one touch dial-in: \+16465588656,,88139848852\#   
[**Meeting Recording and Transcript**](https://fathom.video/share/sjt4UyQtWMEXxTTwg6zzoqyQLL9Pcy98) | **[Link to this Document]()** | [Link to Town Halls Folder](https://drive.google.com/drive/folders/1UBD-b4l3wXfu4rNwwsLw6NiP5hoQY67z?usp=share...
- **2025-09-03:** ...z/**3**+O9j3+Exz++gO27FmFpRznWbWnDqv6pWLSiEY1zClHclIjcmlikl4cjpcSMpIIQxOcGIy4rCCm5OqTnhSCz0IS49CBEpQYgPJmREojU3DCGmW3DXudsuqgqlYvDyVNyuSwsqUpB+eQ0lFQkorgsERlZoUhM1SM+WSvShklaJLK/MSEpGInJei4Oy2vy0TKrid0mEyWVuWidMw2T6T1VnS2JwyhU50ShPjsKLQVxXBzOLErB9NxYLg4b08O4OKzJCENVejjK2Hb7Dq7FzsFVGDzQh+MkDqXEIU8dOipVKpUp5ZxTlip1nDh01OOQi8NLu7FnjyQOj63FkaEuzrGjfZI43G8RhyQMqdchpQ5JHF65KcThybNbeAlSSh1ST0OLNFRMEzdvHpZk4hGrOOQcsYrDvyNxaJGGX4I4TE0kYgQkByWUPQ0dpQ0/jzjksjDNSmY6GxmUNszKHD7pR8tkeagWh9aSolLJ0RwhCpUIaZiMXIILQkeQDBRSkOSgUhSqUYpDShvKfQ6t4jAbpaU5KCvPQ0VlPqocpA5JHjY2VdrIQ0odTp9e51AcOkodKsXhEhKGUilQZZ9BizSUBCGJQBKCMvKylZ0LsHLFQgFNq7Dcpp2Yr2KBoEMIR55UlGRkJ1+2gI8dy+fxdCJJRCpt2r6UZCIh+hTyEqQWFkgstCCShrI0XGwrDLuW8R56Smm4Zs0qLq1IGpLA2rixH5s3r8HWrSQNN2DHzo1ceMnSkIThXqkcqVUaClEoc4jKdjIOkzSUZNqhwzQOsvm9OHJknw0kEodDLRPVqLc/fNh+/8TRYyQLD+LECRKAgpOnBCQFT58+xDlz5jDnNCEtI04RKpFItyV5SBJSyEN230cHuSQ9OERpSFFKldKHJA/37NnMjuUmLg/p+MrycAM75nT8ZXnY2yuSh6u62tlzJ0qWUr/D5ex5pZ6HJBDV8nD+PCpfKvofWtKHUulSWSAKGnkPxGaVQJRRJw6pNKlFGt6ivoJqwaeAZN4XhhCEXBiSOOT3LcnDO6fw8M5pvEqyUIZLQyEFX5OloAqlMFTKQpKH8jKeNHx0kXEJP3z1MudHEm+TNHz9Cn7yxlW8y6Yf3zuLu5fYa+fgRuzd1IktffOxoWsW1na0YvXy6ehbOg3di4Q8pB6HXQum8FKlqxZOxZrlM9G3pA1z6R8dZUQjLUKLVEZ6pA7xIf4wB3jwtCFJw1AfT2hdJ/C0IUFJwyAqS+rmhGB3ZwsGLzeETPSAydcbJr+JjEkw+U8S4pCNIQGMQB8rGkodUvpwEnRsXXAAjT5cIBp1Gg4lEEkchpl0iGXXrymJ7DwsNYGNMYhh82a2PMTArrH1GgRrA3jyUKvxtUDpRZ3Wn++HkouyiOSw7S1QypGSjzIBvlwoBpNQJInIIYE4kScUKalIAtGSRKTyp1wgumCShzMmuTtxfNhxm+g8Dp5jX+bS0H3UD9j59CgEuI7nicNw9vdHa/0YvtZSpdFCHLZJiUMSh33L27B19RIc3tWP80e34uZ5SRzeOIx7Vw/ycqW3Lu3lApG4LXHr4h7cvrAHt5QCUSEP1b0PbVOHVmR5yJOHR0X5UkKWiFwcKsuXHhIJRJvypfvX4dg+W0ge2glEkod7+nFIgZ085AKxh5cwFazi7OUJxBWSQOzgElGIRGsfREEHdslslpB6JcpiUaAqbSr1Rdy8dhE2c4G4iMtDi0hUQsu5WJQFopxEXGDpmWih2yoPRRpR2Q9RCESZvs6ZnN5OSh5a5aESkT60wiWilERUSsQn/XDt6jneAfay74tELfH+GahFoRq1HBwJtRwcCbUcHImJXB7K2AtCJZMUqIXhfxdxOFwfRJttVDLwc4nDEeShLAPVKNept1XLP0JDAtCB7FNvp+YrcTiSOBTy8OnFoYeFJ4pDhp0oVONAGn4lDiXO7F+J0/tW4MSe5Ti6awmO7V6K44xjO5fg4OZ52L22DQOd9eieX4blrblY1JyJOfWpaK1KxLTyODSXxqChMAKTc02opj5EGXqUpAahOEWDwiR/5Cf6IjduEnJivRleyIr2QEakK8MNWTGeyEuYhOK0AFRka9FQYsaymTnYt3ku3rp/GL//8A389sPH+OQDKo8p0lFyz0P1D/BfBBZ5+DSoZd4/Ev4Y7KXJF4tCHH4si5Kf4P333sIHv3gd7752DqvmVyLTxC4gnJ9FuMf3Eeb2HPSjn4Fu1L8g2fdlTEvXY/OcclwcWIhLGxbgTO8MHF8xDYeXN+LgklrsW1SFQfa62jWnGLtmF2P3nBIMzi3D4Lxy7FtQgf0LKrF/YRUOLqrG0GIGGw8umsw5tKwORzsacLi9FkdX1OEEScjuqTjZ04qza+fi0sBiXNnSjmvbVuImO+m8uXM1Lm7qxua509CWk4JCUxAy2Al8tlGP0thYVKWkoTwlAyXJGShITEN2bBLSYxKQGhmLRHMkovUmRAYbEEVo9YhkhGl0CA3QsgslIhhGRoiEUaOHMSiEE8IwSNJQFodCGhqgIVnIRh1bHugXDD/vAPgztL5B0FNqUcP2zaD04eT8Qiyc2oLGwhJUpWZgcko6apNTUZecgob0NDRlpqMxMw01ackojY9GQaQZeeEmFEaZ2LwJBTFBWDytFO/99D7+8GtKHFJZ4B/z55eecztxKL3W1e+TLwarAPx7UL5mxTL1/XxR2N+**3**/TafHUobqoWhRRxK8nDktOFevHlnkLGHsZvxJGlI7LArU0qy0JI4vLbZwsOrA3hIKUOOUhoS63ip0nvne3HvYh...
- **2025-08-06:** **EcoRestoration Alliance Town Hall Meeting**  
**Wednesday, 2025.08.06 **3** pm ET**

---

[**Join Zoom Meeting**](https://us06web.zoom.us/j/88139848852) | Meeting ID: 881 3984 8852 | one touch dial-in: \+16465588656,,88139848852\#   
[**Meeting Recording and Transcript**](https://fathom.video/share/WT6U2XeCkdSvzxRHzJCVQSUsyQ1HwsNt) | **[Link to this Document]()** | [Link to Town Halls Folder](https://drive.google.com/drive/folders/1UBD-b4l3wXfu4rNwwsLw6NiP5hoQY67z?usp=share...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/37381089

---

## CASE 28: KALOMBO-MBILIZI

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2024-08-21:** ...intelligence-dna/?utm_source=New+Atlas+Subscribers&utm_campaign=20c1ffa4d0-EMAIL_CAMPAIGN_2024_06_28_03_42&utm_medium=email&utm_term=0_65b67362bd-20c1ffa4d0-%5BLIST_EMAIL_ID%5D)

****Kalombo Mbilizi**, Nakavale, Uganda**  [A CALL FOR ATTENTION TO THE ERA COMMUNITY](https://groups.google.com/g/ecorestoration-alliance/c/_WWveVTmsD8)

**Proposed Matching Grant for Mbilizi:** The Steering Committee will recommending...
- **2024-03-14:** ...18:00:37 From **KALOMBO MBILIZI** to Jon Schull, EcoRestoration Alliance(Direct Message):

	please Jon, we are working with Vetiver without borders in collaboration with University at Buffalo Experiential Learning Network, UB ELN on geotagging, soil analysis and establishment of vetiver system in Nakivale. Also with Hart Hagan on formulating a compelling presentation about water security and food security by...
- **2024-01-17:** ...we have an [ERA Member Voting Process](https://docs.google.com/document/d/1Wf_4kulyG6WC60H5TfheY5NYjvh3tk5ntY5-7A5T_70/edit) )

  * Two Presentations on Two Funding Proposals

    * [Renew the engagement with Michael Mayer and Jake Kelly](https://view.genial.ly/658e1404d2d6710014ec78d2)

    * Samuel Obeni and **Kalombo Mbilizi** :[Nakivale Banana Suckers Project](https://docs.google.com/document/d/1IseX6UcjXe4rjUYfqVbA5AcNGBHJlEhY/edit)

  * Governance Proposal

    * [Let's give...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/136973840

---

## CASE 29: Kaitlin Sullivan

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/192879914

---

## CASE 30: Kaluki Paul Mutuku

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/263417891

---

## CASE 31: Kaluki Paul Mutuku (2)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...OCquw4uOh+hNMYEXYUeqM90h6/1fuxd9yJs9fYgKZQdqz4TrWVx6KlOwuyREpwYLEFNtheaiwJxcrQU1+dbcPv8Edy9PIbbxJVx3L1+DPdvTuH+rSk8/Hgan9yexaPbJ/DpnQU84pxknMKje2fw6P4ZPGTjLx9dwtdfUYlTSfpQLA5l5aH48t+SOPzq0yv49tNLbNLajYpEL0RbqaLY0wBN4XaoDbREfbANF4d1gXZooH4wJA7DnNAS7oz2CFd0RLqjlSFJG9bE+aE6KRRJ/m7QUNiF9W+9i03vb8SG9zZh/ftbeG/DTSQOuTxk2+vksGWDPEMRWzaqiFFmiMUhScONlDZU5vKQUoc7tx3E7l1aUNytCxVlQw6Xh/LaPH2oJBaHijx9qMtHSh/ukdfHHgUDKO7Vh6qqIfT0LOFi746kiFiUZWShMC4O6WwhnuTnjWhPTwQ5u8DTwQkiOzs4OjjCwcUV1i7uMGPoOrlA1cYOe8wtsNuCMIeSuRk02e+bhYcLnHzc4envgZCwQHh7e7MTmB07GVrB0sQK1qbsREpS0IbKljpznGyd+GVXe1cuDp1tRHCk0qYW9nA0s4etgSWstM1gftgMVnrWMGPbZtomsNRlJzNtfZhq6SDA2RmJwX4oTY/G57fP4J9+/QBffXl7idRaIsl+CKuIsb82/uLiUCINxZzi4pCShovikMvDVVKHy8UhbUvFITvG90lDoQTpKqKQy8Iy6bhwtFQKlShdkEjDVZKGxJxYHM6MFGByqIiLw0g/B3jYGsDBhMShCvQPKODg3i1Q3vEh9si9xxZTqZgeysPMcB4mj2RisD0WR/uSMNaXjOOjObjGxWEjWxCX4eJ8BU6ML5YqJXEo4cRR2dKlQuqQxCElDk/xxGGeWBzmSsucEoJIZJfHKbVI+wR5ODtKl/PZfYrZYjkXRzoS2IK6gPc4JHHYUumPxmKxLGTUFnoyvFCb783ThoI09EBlrhf0d7wCS0ocbl/LsZB7DcZbXoadwltw2vs+**2**/cGROp7obtnB1obKpAcE46OxipkJsWggE10afRysUZGYiiiglwR7GUPf1creDmYwMPGEElh7LvD6DBM2ATUUksFLqaHkeDtgPQgN2SFeCAv3Bvl7L4NWXHICHZFaUIg245GbXok8sM9kBPmipxgEQoj3FAW6408tp0b5ISCYGcUhbqgJNQV+exyjr8DMrytkeZpwUZLNpog1d0YKe5GSHI1QDLhYoAkF33EOeki0kEbITaHEOqghxhPS4Q46iPA9hC8SByaqsLPVgO+NhrwsDwIFwtViMz3w8pwLwy0d7IFw262cFCGmck+mJiw0UwZtrZqcHRUh6NIg+PioYPQCFsEhJght8QHHWPJ+PR3c7j2xVH8Ix7i5ldjuPpZLy48ase3f7zGrjuJa1/3scvd+PTXl/Bv+B3jn/Cv+A4Xb4zj1KVBTM53YXKhHrNn+3DsdB/GTvSjpKYAJ2/dwNytW+ifGEFEjAfc/UxR3xePmiMBaBlLRNdULY4tDCI8IgQBYZQqdIVLgAgWzvqwtDeAh68veocHEB0TitrWGnQMdWP61HFExoWgoCYH1e2VyMtPhLebNTw82MLFwxYxCZGIiI/kf5np7++KMPazCgwSwduLFlm67HtfFyJDNbgaqvJ+hv5mVLJUEId+pupcHDrrKbHrVeCsvx+27HYd3dWoqs9AW9dScbhYplQoVTomThuSMJRIQ0EctuHoVCvGKHlIJUjF5UhlexsKlzvZSJe7OJQ47OkuxPhYPcZGajHYXyIWh2U8cXic5ODJpeKQtmdP9XNxOH9mGH1DVZiZp8ShUKpUgNKEJA+FcqWygnC5NJS9bkWKcDlPShUeUl0hCB8nCg20D8BQ++Cq8KQhu42eGKk8lIhDPYk4pMQhycNDYnEoi1gcMkzZQltWHlpIxaEYC31YcXloAGsrI7Y4N4G9rSkcxOKQy0Nx4pCnDWXEIbEkbegrkzaMCkBsXDASk8KRxuYVuXlJvLdhVbWQNmzvqOFpw5GRDi4NJ6eO4PjMIGZmhzA7NyyFBOLkVB+OHqXSpdT3sAG9vdXo7CxHW1sxWloK0NCYi/r6LC4Pa8TysLIiRUoFlTAtTUBpSQJKiuNQXBiL4oIYFFIJ08wwZKcHIzM1EGnJ/khL8kVKojeS4zyREuuB+AhnxATZIYHNZfMinVHPzl89OcEYyg/FUE4gJildWBWHc4zzFbG4XB2PK1XxuFQWhfPsunP5ITjPuMAgaXizlKRgDO6y296vjMUDdr+HNfH4pFbgYU0cHtSw66pjcK8qGncroxg00n1icKc8mnOPbd...
- **2025-06-25:** ...tixLHlMTxSMIvoJQeAL3tiSptV22J6KglPTcFnVFmvyvm74rYCREzg8aauRUZRA5qv+wPVVuj3mdDi2GqaEAoDyrZQfF7A9XroOqcRRkzL8YXxYQ/ntyVUi8k9HMxg8rXYuhl5MFpgIOIGgtB60rilpL4uQRuWU+sqrAtIAyUoEIlRx5EJMxqHOuO45agK+2PNu6vvQl985DNfwhbicVR1IRuorPNJ1hmEqyT4DE09EM1M63iAEqWoNPFYcuxFjcoiuiOfuGfE0XYBoA+6i9AlmkrGuuyifAl4OsGS1hndemQOpoHQIwjI3F0GHAzhpoVUR6g6hhsTUxvIPay+SWWTTW2pyfCOmxJh82YyEU9OBNrtMsQbtnlEDDHPwDWfplmFLBIP1ozmVpEdAXehvAgBRhN0UnTwlo03heQ2ZZU1KKcnJHYJuXkLGAE8mDQtakNMFQXgQFYeMUc6v4izgN4/Yt54EP04Jjl6LNYBpcFKA99QcZ6DqRPHciaOJgxEZf+CFqC3D4lF+aiLWcBkOsQ5TpIeA8RaB8eVAULUM56wZvB0aIGh3XvF4OCAIYr19Be6FxJXCiJCSeSYTMVRB1fWNaw0QyfbVmBu5COAnoAHSiAAWN5UWUVEdba1vS2SAK5qsfdSmxSTT3UCTNKZkZNuMwsOhR0VTRxlZozUot62q9lohPWWPAYgG7bEgwVWqDUteBVO4LQsxQM2pMUYryGc8EFaNEY/XY8hR5WdIUONHPTRC4n0T49tpBgX9Txcyi/i0rKQPBs7de5ApuiCSj8JtCSyOmKdT6KdTyQpE+jAbhoPZOGC0e7PFzPhpYNaoQJpfOO1Dktdi5JHC6ZfUnDz0J3Bpcld87Jc8MHmPn4qyuxzLTRPpXATpuZ5RQhqGfmIHwYuHU0a55a1LEzJmHGxM8aGa+RWzE5vOBykcAgdrTUupZB46RorBDYlIsgiGR3pcwW9EdoAOBzEuD+0+uJ+J6Z2FPTYSXnRzUqjEsneBIyg6Z0H3gbJb8E3AkGIKsQXEreA+IN/inNmovJfCDOvK+6Nq3OWkD5aTas4BFcxjsQYEnTl0CFquBX04+11FMAuP8esP6RsdTsslF4kP7wp4xHb88U3km0jwBXGYlJEzWR4hwyCU3k+HJZ8PWnVROKtA4zNWPA5rTW+wn80KfV3YXuFefE8rGstsP8AyMxBUyWxHd/XtletORLv7eouFR0hJ9Au+5wVSeu15T73jru7J2+ek9r6Uxiu8xMw5ncxhvht1iPL5XrS6WHk8keA1YijC2VLj07l9tntLam0N1JTBM3spI7vXYuv8tItCUy3UfS27nb7vRHy0nOqkT6DgIs6NgGejwxo+GfWvqK/HvJmY1AfAlMv4G+QY94rk2tH3E2JAA2WtoSyQZuyF+**2**/PwwX5dCdxwTBjSX6k5nddeH/3L55pz6cg3aTxBv0dtqAOuat/75i8qRVL7zOH/PcKUPgCzJXlniW3M8WDpiv5mED57kluP+qeNIRveZksYc91JpIKJMK0/A+48K05rLw0nMkJ5Ei4kVuDZ+33bXwDabqPuyb+6pLQ8l3w3IbR3HC+4mZ4/FWm/G4QNS6oGacRuYFYj6ZnwqiehPoRsPU6UpZEGirdiUVqVPazRau034LT01piTvKqlHenoRoiw44hjSdYBd+tA+HcOOyohuxVc3jtk6T9h69F+16W3DGuyh1rastfpUmCtalAAOa15BzKqIGei3CeSk2TpmsgyYLd2JeFcS2W4k+1TEfRk2L7P6UGU96UYjSvRcHLUECh7gXUqDQ5/QskM6stNo60yle1KI+sNkcxI5JPt2JMkBTnAB/KaImRexC6guhATdHwQ9jRYGBLCjJnR8v56+acD7TNio2XJff+WBzjoN4R9YEORpHP46Dn8rwp5AGFCQM1p8MpnxJ9gWzWl3DtuGj2ODR7CRxLS7urSHSmwOQDOOQ/O2aJInzQAAgABJREFUPuTdH7LhWPqxhHoC0AYEZsK8CaQrgZpPICeAxPW2nmS6N4nsTMI7Uom+o+TICfLeSWwyFVsAdEP+GnFJlHvoNR0FD2IhGXuYartzzDoGZ0zBhxKoW3p2QMXfkgrj8cI9GX9PzU7omAkT89BMR42dUGC3tfy0kprWsktJzhBgq4l8ZMK6DnPQlAfNzJ1EdlFP+jRYxMA9VVE7KmoLTvfz7KHo2BYAlpL0KYiAzPpEgb1QMpvIWduHtHx7gr1PR/aaiNtmaspAzBkZv5HfUuPbOtue1vYkWsm0I2Y3xey6hImAojWS7gRiNgWfOEyMp+AjSfgA/IQk+nYKPpeAedHABLuOxsWoWYhhAJ0Kiw9IV4kK...
- **2025-05-28:** ...**2**/RfW/9OZ/zPk/y0BgIWZu4CU+c/**2**/56wsJQJ4l+A7f05658FALbTAgB2AZgFe7bwZ1t/tve/HVZO3rB2YvLfB5bTcJZI/hmy39ELVq6+0jq3BAtXWp6y+bdy94WVB8FTCWsZW/5P2f7L2To9ALaKANh4B8LWNwi2LABgBwD/UNhz5n9QBBxVajhw1v8U8e8UqpUI//AoOEXEwFkgmtaj4UKtqzoGbgLRcNPE/H/svQWUHNe5NRrLju3YlkkWDzNzDzP3QA/0MFMPk4aZmUnSaMQsW5YsWWxhJNkxxsxMN07ikOPYlmn/33eqh2TnJjfrvvfWe0+z1l6nqAtO1ak6Z/b+9icwT/pLcImOXUTiM1ypM+sSQ9sqlXAUVv7RwuZfWP3PRfkzWUzbx/C2ElxjqWQwmRwfOwcX6mg6x0cLOMWrrf3Z6j+Rbfuj4ZasFKWw8udpNVxmkSLBNTUGbmmx8EiLEXBnpBMyaJ6RzstZDBBJZRStj5SQHiHgRnBNV8A1gxEOt0wF3LIWwz1bgkeOAp65EQJe+RHwLYqCf6kS/mWxCCiPQ1BlIoKZ/K9PgrwpBeFt6VB0ZCCiIx2RXZlQ9uYgfjAPicMFIuI/ZawA6eOFyJgsRsZUMTLXS2XGVBEto3UT+Ugdz0PqaC5ShglD9Jv+QiSzCKCnYM4NIKYtD8qWXEQ3qRDZoFKnA8iW0gFU0IC8PEeIAOZSAhRlwL8wUy0CSBUiAK+MJHinJ8EzlUUA8fBIioX7IhGA5ATgKEQAip8XAQTOOgEw+U/wCYK1D7tW+MPK008IAWy9/GFDpSWLANSwcPdWCwDmMUv4/xxYAGDh6QkLFgJ4LgYvt/KahyUv83KnduMGSx93ajtukl2nnyssA9wErAIZrgLWQS7UjlxgLeBMbYkQKkFE/oc7wkZBiJAJJCX/nAAgVg1JBCBF/icL8l8IAJj4z0tDSUE6IQ1ldD/WlWahskyFqvI81FTko66yEA1VRWhigr+mRKClthRt9eXoIMwKAGZFAE2VBXMCgMXIVQsC5t0AJIeAXEH+N1Yw+Z+H1uo8tNflo7uhEP3NJRhsKcVYWzkmOyuwsacaWwfqsXOkEXvGmnBgohmHNrTh0ekOnFALAE5dLwCYaZQEAJtYAFCDx6aqcHp8HU6OlOL4ELsAFOM4PcvH6Vk+1isR/xIk23+J/Gfr/3U4O1YhBADnJlkAUIeLGxpwSQgAmnCVjneVjntlplWQ/5eoZNv6c9MtOL2hCScmG3B0vAGHRupwYLAau4QAoAybO0qxsbUYE42FGKrLQ29VNjrXZaG1THIBaCrJQGMpIwsNZdloLFehidAsyP9CdNaVoq+5EoNttRjrbMBUTws29rUJYn/zYBe2Dndj60gPtk30zWO0F9to2Q51uYUFASwW6G3DBnYM6Gqm+pYEAGNtdRihfQsRQHMV+psq0ddYMYceegZ6GtTkP60bpW3GW6sw0VqJqfZKbOioENH/**2**...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577

---

## CASE 32: Kaluki Paul Mutuku (4)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...yBeqUZx9SqUkPJLG6CpWI7S6pUIjUrGhClzMXLMZNg5uiMmIQUJCgaHuZCrCiDLKEBcihqpeZXQ1K1FWeN6VK7YjMrlm1HRuBHlDew63CxqHBY3bCZ9DZm6AYtD0uEenUNjTCWNKXVIyF+O5OI1CFaUw9YzCabWAZjrGA5L11jYeyvgFpYNv3gNAmVlCJZXIEhRSeNVBfxJfrJy+MkZHvI8g8My+CfxduUIk5chKKEQ7iGpcPZNgK1bJOY7BmK2tTdm23jC0tkfzt6R8AlXIFKuRkJqEeQZ1O+yGSAymFuG/OI6AQ8LS2pRWFwjiec11SjiiNCiKiENqVhDraYSRXR/lRRLbRHdb6Ul1Sgrq0VpWQ1KSmtQWl6HkrI6FBVXo4C2z80rJZUIMJlDbba6FFlCZcL5mEltFl1jBoZZpJzCGsltWFIHTelSlFY0oLK6EdU1TaRGLFu6Ak0Nq7CiYSXWLF+NTV+sx/YNm7F/604c2bUPp/e34mLrUdzgmobsMjx9AQ/PXBQuQ9YT4Ta8jG8uckyptrYhg8ObDA4ZxjHAY3DIgLCDo1AAwnaY+Dw47Og6ZFD4VFsL8dsO0tVEbAeI7VGlWnDIQFDUNtRKLOtc45DjVDlWlZ2GnRyHN/n73KDvdg1Pr1zBk8tX8OjyJTy4dBF3zp8jnceN06dw8cgRnKb3sxP79uHwrp3Y9sVarKyqQEVuNmoL8tBQXISm8hI0lhejvkyDqoLc/**4**+99wCr6krb/mcyedMmySSZZNLrpNhjiV1RsCCCgAqIgCIKiPTee++9994RQcQOFrD3gl1U7F2jUZPo/X+etc85HFBn8n+/+d6Z97sy19xZu519ztln77XX5ud9PyjLYddhOiryuNZhJioYHObJwWEGyjmOqDCL2ixUysBhNe2norCAlC/m68qLUF+Rj6WlOagrzUR9WQYpHcuoXVaWjYYyCRwuryxAI2l5dTEaqzmutFzUOlzTUIm1jdVoaZbiSjeurkf72gaF23Bv21oc2Noiokq5xuFRWVzpsb2bcWIfx5ZuFQCRY0u5ZYDI4JBhIev+jbMCIN68eAw3L53A7SsnaXknLT+DB7e6BER8ePsCSQKHD+9I4PDX+zfo95S5Dh/eVESW9gSHXOvw31fnsPcfsn/Xf4bSY9OQFpuKlOgUJEYkID40DnGhNAYIjkF0UDQiAyKEogOjEMfgkBTpG4Zwz2AkBsagLKUAZYl5yA9PQ2FoGkrCMpHqEokkhxBku8cgxyMO6S5RSHOiZfahSLALpvVR8Dd1QXZACvUjP+P+lYe4eJnB4X2cuk2684Dan9B1/zHO3PkZB85ex5rth1CybA1qmltR17QOZVXLUFe3AiuWr0VV5TJkZxYiKTYFqVGJKKL7aFFaNkqz8lGeU4iSjDyaz0FOQiqC3LyxoqYBD2/+hLvX7uEW6eKFW7hM7c17v+DK7V9w8ebPOH/9IbquPkTn+Qc4evoOjpy8hSOnb+PwqVs4dOomDp2mtvMmOs7ewvEL93CavkPntUc4Re3ek1ex//R1HO66LdRx/g4O0nb7GRqyzt6klkTLDp6/S/oRBxggcozp2TvYfe5H7Oq6h10X7mLXpVtoPd2JlScOIn5lBVwKY+BdnYSAxjQErEgVUaXBa6SYUlZ4S6ak1kwBDSNasxTgMGZDHhI3F6P0yEpR51CAw7sMDjuw6W6HqG+**4**+c4RbL59FG0kbsW0kttQGRxK0PB3cPi/QQwKWXFB7ojyd0Y0iZ2F6VH+yI4PERAxys8Z4T4MBZ0Q4e2IEA87hcsw3NsJYZ6OivkwLydE+boi2s8NMQEetD93aj0FEIj2o/fg+EAvFwENQxgUejiL6MJwTwnuhTNE9HBEqLujBA6fAw0FOLRjQChFkIrah862AiTyMq6RyPuJoPeK9nFDlLergJLyfXEpHd63gIYMJx1tRFQpA0MPywXwtlqoAIcMdRgcuiycqwCHvtZmCHFagjAXWwTYWgrYYzFLS8SU6o4bCZ2xIzB/+hR4MQCyXghPep2jiR5sOAqUXX0zp8FMgMPJEjhkh99MDVjpa8F2ri4cjGeL7RkcMozzX7JQQEAhmevQ38pMch4yxBQ1EBcjgl2HDA+5LJCoa2ghtuuGhgzD5sLNlGM46TvN0xdOQ4e5s2CtPwPm2lNhpjkJCzUnU8tgkF2FEjgU8HD6ZFhwVCmDRQEO1TBv6kSYTZ+EJbO1BJRMpd+9PiuJlCzAYZg9g8NZAhra6+tItQ3pmApo6GaLrEAPAQyrkyJRnxaH5rw0rCvOxqbKQmyrK8Oe5TU4tLoRJzesRtfWjbi4s43Ujgukrh3tOCvAYRs6ad2xjetwcG2zgIc7GusEONxYVYrWimLR8jwDxK311dhQWSJiTMsTIpBBnyHaZYmITWVw6G1uLDkOZU5MCRyy21ACh8I9SN+fIaACHHIEqQ5rqtjObs4MmVtRRyzjWFNTTTXpNbocS6sJW8OZcF4wFx7m8+ncmi8gtIi4pfMuhH7DeF8PpAT5ITUkAGkhgUgPC0JGeIiAh1mRYcKBmB0dLuoacjJHSUqiBA97iV2H+QkMDmMEOEyPCJdBw2AFPEwJCRL1DeP9/QQ0ZIDI0JAdh0m0LjU8VMSSsruQIWFmDNchjBBuxLTIcLGclREVTvOhtD2NBUL8ER8kQUMGiFzvkGEg9wMMC53oO7Pr0I/PV28X8Y8KGCwyPOSaqAwQk0L9kBQWIJTIoDe4Z23DUOo...
- **2025-06-25:** ...y7kfL9m5sPP+kfbb+9dvn1c0e1qkb/PVLzYFLs+rCNnOBovPBZeXVm1asGGe2TW1+3rlla+3lxx5q2D+G/tOLL76xanemweXrbXkM+N3H7Nc+qzk+jcl9ZEZ1c3Ly717TrfVbGxsnjB9S7p15cvLtq1q9tbc6DkW8L/BrX6ePjSCrdXy3iQe9lhMt4ZH0G2pNMSPxDFVdFqIgBVn6wYzUPG/rOQnfgQBYNVTNFIj+MJpPwEs2Ml7Up0ityHT4h7J1I8wlGVM3p89Zc9oQ2nGlJ0Z03YhZebuzsrbg4RmgEjkGAmdF5U1bfeI3F1IOdN2EqHjkXm7pRqVv0fUaMNeUY8Z94l63FT6hHn/GMsBqcZaD8YEx0/SSIdI+xRzSDyOa9G/nmIPyFt4ALNf3sID2FJ4ALMPTuJ2LL13LF0qbx9nDuTQB0fYjj/mPDHSdjiTLk2zlmaxx0bZy7PZKkSH6VZ3qsUDBf8gjQyWPUp7QpwXE0kELJGx4oez4fSjAVYcY31vwCIi5ljPYsBiESu0EakxYCHwTIN92psyOW+qvS2nIIS+zVfm7N3c0L7qjGfKkgPjHbtG2o6mOcpVBdXKglqVq1bnQLjdkMM2wfhUgJ5Y85jzfA696xdLDy5vDM4sO/vCrKVPF20azR9PZxpUfCTJ1UEVR6jikNopGTxiZTwGUcsI/uzrMzeuqz5afu9U469OVt84HvnC7b1ed6bz3NwjGz5ePvdV1/SF+**4**+5r/TV93bSi9dPnFrwgqHodcZhnuc419ns/vrbVd7LLyw+o56yaO6hg9WXwzVXLs/YV/usvWoMU/bqjDUn22tarhzourm/**4**+7ZS9/1+O9dO33xnr205QnHsQy2Qs82wZJjofAS+hpFRyAoziP1vQFLSle/h4AlXAq/Fr4lICaCFYoJMxYN4cIkpi7FVkOxZyjmjIar0NPladOOPzZl/4v529/KW5pLzzLbuXxb7hRX3kfT2beKCl6wFY9nFoycsjT9vU3ZU0+OMrZkGENo6EpGVtJ+lrKfoOzHKNupFLpKbfakGtpSjR1aK0wMhgYs8TywFA7sErqKhQjDBLBSHR066GaNI+3nH7cfH8Pvfrlw1qZzto7Plrm7F83dyL7tWP0Ku9L8CRf6bH/fr9avP/6yZeaT9f5F33w1/2r3x9Gw4bP7qxoaTFdvze28llfle/bzX03vuzU7tzizaOUzfReZX3/tvHohrzVk7e3eVucrm7X7zPiiQyPtVZl2b6bN/xCABfvyxu7cYfST9WDhPZshAUthaQLAIlUV6DBlgpJsatartVbnMGdfnVtv2Riaud2z7UhtXVOwwRN0+yN1ntbS43Xz1x37yLXjFf5QTu7hTGOtclqTIjegNLdTUwNqayfk/xnbVCZYaZFijqSYhb2cVaZmJFxJBO7BJAtUZ0Bgh7dGDqmsUY0liib3etajsdUq7bVKp1dhCyu5Xr2tD41Jo23nx/I7Ppyz/Fzj0Y4LlVVdTQsOHHmJXv0mu2z7yW2+niPtN8sP1h153bZm9NTV4yzzFx087W7vCfTeNC3e+5xlzQvWtTO2naq7Gqm/5F+562jxJ+sqw2dDNys6Pqvo...
- **2025-05-28:** ...hy7cBylM/xqRzsL9ERviy3SpQJCHMzwdrOFOnHrYmcLLngVTBzME2JvB35YFZ/**4**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**4**+t+frWDN09W8eJoHs92ZnF/ZQyDnQ1orMlBRUEyyos0uFafh...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577

---

## CASE 33: Karim

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-01-08:** ...Anekha Goyal, Nancy Lee Wood, Donna Nelham, Sean Petterson, Eliza Herald, Ir Marius, Serenity Cooper, Lee Golpariani, Harriette Brainard (Regen Hub in Gambia, other projects), Fred Jennings, Milt Markewitz, **Karim** (Guinea Conakry), Geoffrey Kwala, Kathryn Alexander (Spokane, WA)

**Agenda**

**Happy New Year\!**

**Michael**

**Uganda**

**Phoebe and Master Classes**

**Grant Amsterdam**

* Introductions Updates and Presentations

  * [Samantha Power](https://www.linkedin.com...
- **2024-05-22:** ...I would suggest the at the next meeting we invite my partner Abdoul **Karim** Camara from Guinea \- Conakry be put on the agenda to present the WUN structure for your consideration.  
Jon Schull  
5:46 PM  
5\) programs, projects and practices consistent with OUR core values  
Jon Schull  
5:49 PM  
a) bottom up, not top down?  
Elizabeth Herald  
6...
- **2024-03-14:** ...Elite Projects vs Indigenous local communities left on the side lines of our digital canvas

18:27:51 From **Karim**  to Everyone:

	Reacted to I appreciate being p... with "👍"

18:28:48 From **Karim**  to Everyone:

	Removed a 👍 reaction from "I appreciate being p..."

18:29:03 From **Karim**  to Everyone:

	Reacted to I appreciate being p... with "👍"

18:29...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/274249468, https://fathom.video/calls/253037687, https://fathom.video/calls/214451149, https://fathom.video/calls/201817513, https://fathom.video/calls/209204233

---

## CASE 34: Katharine King

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 2 meeting(s)
- **2023-05-24:** ...Imagine if the **King** James bible had translated to man's responsibility to animals rather than man's dominion over animals.  
16:10:18 From Lee G to Everyone:  
	I'm in a big cube farm at work so I feel a little awkward to talk  
16:10:57 From Lee G to Everyone:  
	https://encinofoundation.org/  
16:11:29...
- **2023-01-18:** ...Maya Dutta, Caroline Petruzzi McHale, Paula Phipps  
---

## **Agenda**

**New member [Adriano Wajskol](https://docs.google.com/document/d/1W9fQFMtzCXA0bEKC224kuj2nMMa_ubZiqac_oM5mJpw/edit?usp=sharing)**

- Italian Film producer, documentarian,  and **King** of Development of the Asakyiri Royal Family  
- Chief of 10,000 Cocoa farmers and 50,000 acres of organic farmland


**ERA Steering Committee Update {Ananda}**

- Proposed Method of Creating "official...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/151504382

---

## CASE 35: Kathia Burillo

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/168111809

---

## CASE 36: Kathleen Groppe

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2024-07-31:** ...https://form.jotform.com/222647520358154  
22:04:59 From Jon Schull, EcoRestoration Alliance to **Kathleen Groppe**(direct message):  
	Kathleen would you be willing to go next…?  I need a dose of strait-lacedness  
22:08:20 From Jon Schull, EcoRestoration Alliance to Everyone:  
	https://BigMapToSaveTheFuture.org  
22:08:33 From Indy from Cosmic Labyrinth to Everyone:  
	https://www.cosmiclabyrinth.world...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/127857495

---

## CASE 37: Kathryn Alexander, MA

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2024-12-11:** ...Colleen@rainbirdut.com**  
**21:16:17 From Mark Haubner to Everyone:**  
	**I'd never want to be part of a club which would have me as a member**  
**21:17:01 From **Kathryn Alexander, MA** to Everyone:**  
	**yes, please put me on the email list too\! soilsmartsoilwise@gmail.com**  
**21:17:37 From Mike Lynn to Everyone:**  
	**likewise please, mikelynn201...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/218283603

---

## CASE 38: Katrina Jeffries (5)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...sKkMw7TvM00UoyJnGG3bWcLUyh4OFKcwN9cQztIgGyCXsIBTgMF8BDwtomR2FDBULn4ODkvg1rDyUVihUyaEXqayW2lnFFblCJZWSOoYbLa6QxGCQVSokR1lHVcpRroCESlWxarJRXZuNmvoc1ArRhKMhBw1NuWhak4c1awuxtrUE6zeVY+PmSmzdVoMdOzlE6Urs3duEgweb8e6763Di2AacPrUJ585uxcULHKJ0N65d2YPrV9+UwpR2AIeff/QiMPx/AxzGZRQLMRSMIUWnFiAqOR8RSXmISMxFWEI2wuKzERKXieDYDATFpCEoOhWB0SmSolLbFZmCYFZ4Enx8IqCvyG2oqWKA5Yu0sWiBBpYt04GxsR0Cg2MQnyRHQko25LmlyCooR3ZhOXJLKpFfJsFDrrOyaR1vw8rOrYCDow+0dS3g4x+F2MRsxHEew+RsRKXmIDI1G5FpOYhmUT02jdan5yA+PRfxGbmI4/ZkOcLiUhEak4ywWM5zSIpORigrKgkhpODIBARFUp3W+YUnwtLRF9qmTiQXaJm6Qc3QBaoCHPpCwyoAatYBULFhaBiApVZ+WMbLdoFQlQVB1T4QKgwLHQKh4Rgk4KG6XQA0qVxBbdpOwdBlcOgchBUyX2jKfKgeAGOvMHim5CG+eg0iSuvhk1kIj5Qc+Mnpu6qoR0JtE+Ir6+GbmgVzr0Do2blA5hEAR6qHxCQhu7gcJVV1KKuuR2UthytlcFivAIcNWNkgqbGxCU2rVmP16jUCILLjcGNrK15fvx6b12/A/t17cOrdIwIcnj92Eu+/ewyXjp3CpSPHcZWWb5w8g49Pn1WAwwsiZKkkdh9ewbcf3sJvAhwqcxz+iiekp79J7r2Of1LuQIZuXH/Wlo+QxQY9URf87ZkE6hjccZ5ABnAC2vFKBWUTrO6ZAJSP6X0f/fSLAHLK/f/1+**5**+SA5LDj/7JsPCRBAvZeaiEiL89ouP9A0+++V7kOXz6430BPdschwwNH9J+/vhD6NlDDsPKx9RBdGx4ylCRj5PXM2hUvO53dmAqXIyPn9J6KXwrw8m/Hjyg4/4ZT+7/2gYO2TH5B53H3+**5**+i58//wLf3LqF2xcuCN06dw4fnj6NyyeO44NjR/De4bdxfN+bOLR7J959czfe3bMbxw/sx5bmFqypqUVNcTFN5nMEPCzIyER+WjryOkDD7NR0ZLP7MFOOPNouLztPKD8nF0U0Pi4tyEVZYQ4qCqmvLMlHXRlDwxI0cYin6jKs7qA1NeUkhoflWFtfQapE68oqbGisxsamdjE8ZG1uluDhtrUr2wCiyH24niFiI/ZsWtUGD/dva1E4Dxkevo6jeze/AA+F+5AB4jsMD/fi/SNv4dzRt3D++H5cOHFAwMNLpw7h8pnDuHKWHYjHcOPCCdwU4UtP4vaVU/jk2mncuX4Gn914TwKIH1/A159cErr76WV8c+cq7n12jfQhvv3iBr7/6hZ++Ppj/PzNJ/iJ9PO3Cnj4/Wd48OMXQp1/yP63/jXUGRy26c+vO4QxVULCzvoa1...
- **2025-06-25:** ...wUJ+R8FS35JP3kuNT2v4NdRr2Ah1hdqYD7f/Pr589YtXsITDWvx+FF3+EHq0QgULg0xi4asousCwkdOkgaBDm124N6Tdr/euV+fivrBKPVaajTcaa7V6jrl0WQEeDrcJjE28IXdpHPoyskrnQqbqVzjSTjwzG8cJt82oCR6aO5fRZADmbj+dc8R3ArULIzjmWGR6zMiEqLSBCiWoWj1ci4rHDu905/oeWW2PjU+WIZRDAnNpwnQrz9Sgviuiyi5Uv/DsJLooy0gUDxQ0BPVOmTonGwlT0AC08shyzK4J7r9uKoszlSaaSGONBGF+LVPc7G5jJI3IDDcXRbFSy0I7JszEPpvM3dxl1Q2SyjYL93hU2UxdU/aFx/oNDB+KKjXkp9AFhUbCJFFFRUBXt5U0n8IpxNmlMASZvPw+j4aJnV5xBtwgAiueDhce8K0PaF09G19JFQTShFGqDu+cuPMJjWEDkwdC4hmCdP0LGXi7IjS5zGRJIb1XXBtaqUI/OoKe39fpn60k2BebSdNdqyecLl7d41ZG4WZT4EI9dro+mExzSqXJorzbx8L6r5lIwrAOweayCq3zRRj7FtR2MdzUc5ld3l23TqeNGUobMFDbNvsefeiGFuuqBmtMdW2c06maIYc9oIOekTMnVOdtaha1AeoKtTHqNWyMelSpx9Z/iQw1tfpZPvQr/NBiP4mPjQNLHfUI+Nlq/xtQm770Vxh6N5H7bwL1CdQ8MDzVDPDaSLfqJhF3yIA9SmJdxjPRQ+nkNmR4C39QU4JG6rARPGkKT1KBAUOwD4UE9RF5vVhE1W1LU9y9TdL9hVT1qCHuVnXkQnoJPLRMr65DvT7cuxW5+gVyAz1vU81F43QJ416rL20lIl2GzH4Se0hXNIK+y2eoMcCXDcRo3Axh4EGieFQ1bBuvdyu3YzvSgXPt1pE0bkWqtMVNGvw2HdGYJnxtO3J1q2BA16l/O9SmB3XosdoIQLe2fQeqPtrouQR0RZN3ZRs4sR0YU90MhcYwYD9G1L+Z24zaJEYwqAWoZo7Sh0ewyOhfvwaq78wgqpt6vB4MrLrqpnthmMSZ1HNswCN1ukiZnqhek9+tI/**5**/uXvv57aSLN9TVRJJgPDe0InyUqlUkrqquqa72pWTRADXOwA0EknReyd6it6IXpai6A0s4eiNvC/TZnrmxezG7v+yJ8GqmX4zL2b3/boRJxAQBN57cW/mOZ/vyZOZW4eoTTG/G8eEYvBFGQnd0K2zBfREWMm4ZIAOvEfFeiVAA6RfzW+o2B2xbUtOPVYw2zJU4OVTkj4gBjUG998rx+FWeDWcC1jwoH3xQObygfTlD3ivmApobCG9NQRfk1D+A4IbTMEEQSbFYTuxtuexaa+V+HMzGQBmUn41J/8WUG9D6diVpy9K+Ukt5VJalmTEnJpzyQmX6NKyIi2kIXaU+JaUCB+0zcexM/HOR/GOiXh2Ip6aVlIeuBUSfl3mWFPZfSpuQe90K52BGHpdYn8t59+pmNdoQBkLwo+VCZ7Y7OCh3NABZv4g65IKIZUQUrPLGnpSy4zp+RElNahiHmhZl56Lbr5ELqrJeyritp6Z0xAL0rQZg+CX4suAp7G47yDmiyUDByzuWBtKtomtS0raH5e2oOXWpJY1SdqazAaQFJBS7ngKoHkpXvCKOF8M5RXRIRG5Ap+r2GWEVviElJyWUPPwCVpTlAhK9qsjgKV+Tl8hwJLjHjnuk2P/PwSsfz/If/3O/0f7T/7tvyLI/5v9V8T57yx6luB...
- **2025-05-28:** ...itvGoyji/MgPA0XR9kd+5LtC8Vj7kR8GTOznyGL+Gazan4n+cjLk4n9qEpKpr8CE/1HxP1YQ/yMVY/+**5**+O8Od3dn3ucYFf8tWey/Ka/8NzExhCGrdlIQ/zVUlYUqZCZYEqqE8szpo+L/swwA42P/v1MDwNfsSy74/5AMAMzwwFMSniHaf5c8Jf4rGACmcvGftWw9q/4XhP+ZM6ZDmcXfa6gLVf+j4r8hREz0JyTGRpCKRLBgmJjA2lQMR6mU+qV2CPfwRFpIKEqTBfF/RUUJNsyuxNb5tdhZNxt7Fs/DvmUL0LqyDu1M7K9fjJ61y9C/YQUGN67EEWJw4woc3bwKx7fV49TODTi3ZwsuNe3Alf27cPVAA64d2IPL+3bj/N7tOL17K07u3Ixj2zdgcPNanhjAzABbasqxND8L5QnRSA7whj8zAhjrQ6yjCZG2Joy0tWCoow0DbTp/NDS5+K+hzMR/Vagrq0BdiUHnEqE6SwkqrIqfTRWgqgI1PrWGABf6ZSaA8eK/YACYKPqPTQEgpAo8T/xXnfkM8f//hQHgWzB+KopvawDgBpRvawAYJ/**5**/3w0ARiJdGJno8XhrS2tTWNMYz9reFBa2hjC30YHUVpvQJNRh5agBKyfCWQMS25kwtpgGA7Mp0DGdBC0RY7KMqdA2mUYtYTQFqrovQlXnp9DQ/xn0aLtIOh1GZlO58K9p8BNo6L0AY8lUOLnqICTMisayjoiJc0JsPMMR8fEOiI2xpXuXPfLyvJGS4kj3LWM4OEyDvd0k+Pmp073OBjm59ggJ1aYxshqNhbURFqFNrzdCYrIpouL0kJVvibJqJ+SVWCKn0Az5xZbIzjdDepYpMnMtkFfkgMx8ewRHGsHNVwOuPppw8dKAnfMsmEh/CjPrF+HgNgth0SLalz3Sc8yRkWOGnHxrFJU4IzffGUnJ9vR52DziU6Gq+gJUVZgJ4CdQUvoJPaa/VeOn0NWdBGtrTXh4iBEQYEn3Y3fkZIUgM90febkByM3xQVFhAIoLw1FSEIdlCyuwcvEchPq703VQR2YAYGkiatAl9NTVoa+qCm06r/WVZsBZIkJedCjq8lKxODsOK3PjxxIAWPx/URIay9PRWp2Fztm56JtfhMFFZRheUonjS6s4J5YLBoCjiwQG55ejr6YIbaU5aC5IR0NuCrZmJWJVcgTmRPqiItQTpaEeKI/yRW18MOYmh2NBRjSW5CRgZWEK1pZmYmNp9pgBYH4FhtYvw8VdG3C7eTtu792Cu41bcb9pG25uX4sbdB2+uWklbhP3tqzCa9vr8Wj3BrzdsAFv7lyLVzYux+36hbi7rg5vbFuJRzIDwKftO/D7vkb8+8A+Xvn/5yGZAeBYO/**5**+oktW8d+DL8704cnZfg4uHOawdZ+f7sWX5wfw5eUj+OL6UXx56zie3D0JvHIWeHAReOsy8O5VPHmfpQDcwJcfyaYD+PkdenwXeO+OzABwD0/euYe...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/58214677

---

## CASE 39: Kethia

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2024-03-14:** ...These solutions need to be brought at the same time

18:37:04 From **kethia**'s OtterPilot to Everyone:

	Hi, I'm an AI assistant helping **kethia** calixte take notes for this meeting. Follow along the transcript here:  https://otter.ai/u/SQhfNb2winirAU4167DLkfj6CTY?utm\_source=va\_chat\_link\_1

	

	You'll also be able to see screenshots of key moments...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/76758727

---

## CASE 40: Kevin A.

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-17:** ...If no concerns or objections are raised within **a** week of the presentation, the presenter is considered to be accepted as **a** member. If any concerns or objections are raised, the board will then consider the issues raised, and if needed, vote as to whether the entity will be accepted as **a** member.  [More detail here.](https://docs.google.com...
- **2025-09-03:** ...If no concerns or objections are raised within **a** week of the presentation, the presenter is considered to be accepted as **a** member. If any concerns or objections are raised, the board will then consider the issues raised, and if needed, vote as to whether the entity will be accepted as **a** member.  [More detail here.](https://docs.google.com...
- **2025-08-06:** ...If no concerns or objections are raised within **a** week of the presentation, the presenter is considered to be accepted as **a** member.  If any concerns or objections are raised, the board will then consider the issues raised, and if needed, vote as to whether the entity will be accepted as **a** member.   [More detail here.](https://docs.google.com...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/120266996

---

## CASE 41: Kevin Li

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-03:** ...5IneilEocByKXP8a+JQ4425LSgLOqiRNQgS0CWhgzLwpaahkGtog15nXo7IQ4b1eIwViUOk1E1N5UGsBmonc8RhRxhqBKHanmokYbpqGlOQ9WcJJTPpO97Gg186Hh5HP2oEodpVZyq1BvJpZ5IKKLvqsAJsXnvisOoTJ7mqEOVOMx3QkK+M5IKXZFS7K4Sh97IrvAV5Fb5I38ii0NiYiC1QShkaVgdgvzKYORXBKOwPATZ+X4IDDKHg+0oOMnHwNV6HFwtx8HdfBw8zcbBx2Is/IkgWhZsqYNwqwmIlekjUWaEZI04tEa+sw3yOe+/qyOKPdxQQh3GEjpPi6nzyBIxnzqLGQ42SJSbIdpcH5Em4wUxphOQYKGPVJkhMmxMkW1ngXwHrjdAnX9XO0z0VGrEYWOID5rC/DEtLJAIEvJwcpAf6gO8VOLQWUQnTvR0QDmnKnW0Qa69NTI5RSlHG8pN6X0TQh5aIoXWcZqPHHcn5Hm5osDHDYU+7i34eaLQ3wsFAm/CB/k0nePtiiwPR2S42yPNTYFUV5aFNkgmEl3kSHCWCXg6ztkaca407a1Akr8DkoOcqBPuhvQINxQl++Hw1jn4+dlxPLmxXRNt+OTWNjy9sx3POdrw/k58pxKH3P7wUFsc8vRuvKbp1w/34vUDCSEQOaqQtlfzjjh80CIOX3K04b1dgud3d7bimZY4lOThtlaw5GxLW1nYFiHz/g5tpd/D/wZt932fOFS/xnul4f9lcaiRh+8RhwItceg52lrQKm2pljj0Y3E45l1xGDhOLQ9tW9BVIETUQLQTrRR5yKlLpchDlogsD2NMXRBrpsYZ0WYOiPkHRJsqxTax5nS/Zng5RyVylCLXQLSh+5e1Ew1qOdLQDtEWtgg3kyHM3JruG3KkuntK6UoJIQ59pWhDJsmvdfrSFJU4ZFEopCELQxqM8jaJ1G9Jpf5tZlQw0mKDERbuBQcfGziEOsA+2hkOKZ5wzPKWxGGhLxxyfGEc7gA9P3voeTnAwMMVpp6eMPf0gcwrADbeQbD2CIS5sy8snHxh7x0G14AYmNu5w8DSHqZyB1jaOEDp6IaQUBpUZ+UhKT4JPu5esLPmdG/O8HXzIrzh7+mrEYfhIZGICosW0jA+JpHGJKlIS8lERloOcrLyUVhQivLSKtTVTMKMpllYumg5NqzZiD079+**LI**/iM4ceQ4zp2UxOEV6lfeuHAFd69ex/1rN/Doxk08uXkLz4gX1L/9jvq339++I4lD7uNydCGLQo4uvM9Rf4xKHApRqJaAKilI/YxfntC6Jypx+PSRJAyFOFRFHYptnqhqHqqiCm/Ta924I/q1r/lHclzTe88B3N+yE9dWr8eFJatwibi5aiPur9+Gu2u24NqStbg0fzkuL1yJ68vW4c5aui9s3oVXuw/hx2PUj6a+8s83bov3LCTl8+cidSnXPvzbz29V6UU5BSnx82tJCP7M099L/KolDfET8TNoBf72i3pfKT2pJA3fSNLwl5/ENEcj/vT8CV4/vo+X927TPZC+4zu3cIP6tyeoH7x70yaspD7ybOorT6utw+TKKpFatCQnGznJSchOSqABfayQh4KEOCRz7aK0VFQUF4qUpUx9VSWmNNRhxpRGTJ88CaV5ebRvEvJT01CaxTUNs1FGxyzOyhCykCmkY7QVh9qUZHDEYSZKs1keZqOqQIo4rOaIQ3qPdfy62pRxytIyIQ5ZGKrF4cxJk7Fy4SLs274DB3buxi4aG+3fvQcnjh5TpSqlc5PGAOep33/xwgVcvsji8Krguqq9dvkKrly6jBvXrgmJeGDffiENDx84RMc5TvufwOmTp3HpwkXcvnUHjx8+xpPHkjh8/ozTlL4QaUu5fUF/f+Yl8VydupR4eJ/6xVeu4NSJEzhy6JCg7T+y...
- **2025-05-28:** ...9NUrgc+P8Mt3n+Bvf/oKf//5a/z1xy80Ivrly3tyDJrlN1sri6Sr+OhJC3794XP88y/fq/tB9v71SNscjMKEZcjaGYLk2AU4viVMa0MLBS5PyuVT2xfJNgSZO0JQEL8EeYmRSN+9VEB2HpK3LUR63FKcjl+O1G2LkLRuLlLl9tPymuePrEJdxia0luzHnbNJuF8ahzuV8Wiq2osl64Iw0GM4hrFGy9cZ9gHuAj2T4Ch/woyUWguY2nmwVnQsrAVKewgEsp60C83zRwzDCJ8JGBPohfEzfdSmaPzMSTppMN02Ybo3xkx2VaEDgU3rM/vS+7O7TBhd0JFp9b7dNY3fjfWlDkPRjxFTprip5Hd3hJXnaB2EUptJLpq2s54osMquSKMFYgX4KJrqOqiPQumbaKkphW+GUto5EUxVsCQTliU7Lgn4UVjE2leKjLoTSocZHZ1Yy0kTfAKsJetJ+TzTMENpH0ZJrQegj3w2QixHL6b+ZXST1+lCIZUM9qxntNRu7EgMY497U81tf0crNc3n0OcwWkrTfUZKmfofRvHVAAwWAKc9znAvQ+Q0OsDNqCmVQSh1muGpYievsAB4BU+Fx5xJcAtyw8Spzpg0xQV+U5zhPmYwPEb0xYyxw7DQ3R4xfs7YNX0C9s32xPFQX5xaRDAzYFGBzAylTNezregq2iEZtaCGsTwFP4TSmTB63htRUoqXCJLmKCm7MJXIY9SfNJy2UFPUOJ+epdrjnq/FFL4JLM3pe7OJPgVUjJRmLJqsYJqxcLIJNFkjatSUapSVz5OhanvaQ61mat54PdaVmlX5jJ6aI7Lcmt+T7UV1sPsTP4d6qpoh2lwD+zaaqq1Hl5tvM4H6GsOrlO1EC6PmvLGC4pZepQVrjBaubDGqUVRZbJ5lat4EpeaaUgXPdqr6/zTaq/B5vZD1pAKkjJASPgmimSsJpTM0YkrRE+87ETENycsCkBwZhOTlM7BHFjLr5He0SM4tV+vesBOQ69+**lI**/p27oTunZiyp7DJUqC0C7p3EzDtYoEunTuis0Brp45sN/qe1pdSiW9AqVFXSucKLtaGjRmui7FhLNGRhdjAUVbye7ZX1bzrTFk8zfHRQeh0lsUxzw+KnQilFEzauI7AaAFDV/lPGT/NC04CqEPc7HXYuMlibSL9T50waZYf/BdME1C0kwVlL7zfvQM69OyIjr3f1pT25P+W3WB5fSNS2k8WhWoJ5TJc60ntxo/EjEVzERGzCqu3RmPmwplwnTwe/nOmYsnqxQiNCJXzygMDBWwJpfRhtZEF57tAqlC6LiwIaxdNx9rF0xC9OBAxS4MQGz4Lu6Jk8loZisyDm1CQtkdgMx4J9JnauBYrF83GhiUzcWhTJJLiY5B2aLsagzNSmpd+AOkpexEbsxwLw2ZiRuBkhM2ejsVzp2FZsEyA8tyoiGCsjQzVetJdGyJxZPcGZFM4lXHQMKkvJoSdNIFplkzqKQKdh5B3gi0Yd6uqODVxi0Lpsb0btRVqeV4SinIOI1fgOEOgtPz0PtwWyLxvTqlfK8L9lgq01tGKqQDXrxSgVsD0wbVSPL5RgcdNFWi+SnU2RT9FaKw0esFrV6CLOQKh2Sp+qhdI5bhOAZRAKb0+qV5n3ae5jpTv90h71p/HyweGd6Sq72+cfaOIJwS+uFOjamum39nFqVWez9fgaKyiCCpDjkOaglZ18XG1O+K4WJiMitxDqMg5gMr8I2pnxU5WrZfzTVE3I7JJkDRaf/J9LiuUsj89r/O+xzfZvYmdnM5rhJSRVMKouW7R2BrpYXYJevWAve0vKZg+vV0p8HYJL+5eVIETSwkYxSU081ix5II+rkwD19MaSgC1uuQU4raswpboxTi8PRpp8h1mHtuD3NS9agNFX1KK5c6k06uU6fxkXCwijBvCpt+r7412o0zTs4MVrcHOyW+Ax+YSj5mAaRW3JWxNyxa0Gbh1tUTT41+8vI0vX93D568e4rPXj/DJS44n+PiDx3h6rxXP7zYLjLXik2d3tWc7wfSVQNTDO9dxv/Ua7t6sxR0B0ds3LgmUXkSb2hzRiqkejwRM6Vd6...
- **2025-04-30:** ...I visited the recent  ChangeNow Conference in Paris and thought this campaign was something the ERA could get behind.  
        
      [https://www.linkedin.com/posts/grant-holton\_makesciencegreatagain-makesciencegreatagain-activity-7322591520002379776-Kjvz](https://www.linkedin.com/posts/grant-holton_makesciencegreatagain-makesciencegreatagain-activity-7322591520002379776-Kjvz)?    
        
      Moretreesnow in the Netherlands \- [https://www.linkedin.com/feed/update/urn:**li**:activity:7322591520002379776/](https://www.linkedin...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/120266996

---

## CASE 42: Kim Chapple

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-11-08:** ...And joyfully  
16:58:42 From **kim chapple** \- great lakes bioregion (cleveland, ohio) To Everyone:  
	Reacted to "And joyfully" with 💓  
17:00:18 From Jon Schull, EcoRestoration Alliance To Everyone:  
	https://docs.google.com/document/d/13vVMvEKSaOMizLJuWHpccJeAGo6GXjPZ7LkZbhcVXJU/edit  
17:00:29 From Louise Mitchell (she/her) To Everyone:  
	Your work is Powerful, Nawi\!  Thank you\!  
	  
	For Everyone \- Re: the Nov...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/48059317

---

## CASE 43: Kinari Webb

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Not found

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/48300403

---

## CASE 44: Kwaxala / Pete

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2025-08-06:** ...If any concerns or objections are raised, the board will then consider the issues raised, and if needed, vote as to whether the entity will be accepted as a member.   [More detail here.](https://docs.google.com/document/d/1vz42jQ68k1_WWQJzE8W7UXa6tG_9dazTWDZSrP0oEas/edit?tab=t.0)

**Participants:**

Jon Schull, Alexa Hankins, Hart Hagan, Louise Mitchell, Mark Haubner, Fred Hornaday, **Pete**...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/373972665

---

## CASE 45: Larry Kopald

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2024-06-05:** ...What’s your actual name?

   15:03:07 From Jon Schull, EcoRestoration Alliance to Lastborn's Galaxy A11(Direct Message):

   	(Greetings)

   15:03:23 From **Larry Kopald** to Everyone:

   	Hi Ananda, great to see you as well.

   15:03:55 From Tania Roa to Everyone:

   	Hi all\! Glad to be here.

   15:04:04 From Jon Schull, EcoRestoration Alliance to...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/104999059

---

## CASE 46: Lastborn's Galaxy A11

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2024-06-05:** ...15:03:01 From Jon Schull, EcoRestoration Alliance to **Lastborn's Galaxy A11**(Direct Message):

   	Hey there.  What’s your actual name?

   15:03:07 From Jon Schull, EcoRestoration Alliance to **Lastborn's Galaxy A11**(Direct Message):

   	(Greetings)

   15:03:23 From Larry Kopald to Everyone:

   	Hi Ananda, great to see you as well.

   15:03:55 From Tania Roa...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/104999059

---

## CASE 47: Lastborn's Galaxy A11 (3)

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-17:** **EcoRestoration Alliance Town Hall Meeting**  
**Wednesday, 2025.09.17 **3** pm ET**

---

[**Join Zoom Meeting**](https://us06web.zoom.us/j/88139848852) | Meeting ID: 881 3984 8852 | one touch dial-in: \+16465588656,,88139848852\#   
[**Meeting Recording and Transcript**](https://fathom.video/share/sjt4UyQtWMEXxTTwg6zzoqyQLL9Pcy98) | **[Link to this Document]()** | [Link to Town Halls Folder](https://drive.google.com/drive/folders/1UBD-b4l3wXfu4rNwwsLw6NiP5hoQY67z?usp=share...
- **2025-09-03:** ...z/**3**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**3**/TafHUobqoWhRRxK8nDktOFevHlnkLGHsZvxJGlI7LArU0qy0JI4vLbZwsOrA3hIKUOOUhoS63ip0nvne3HvYh...
- **2025-08-06:** **EcoRestoration Alliance Town Hall Meeting**  
**Wednesday, 2025.08.06 **3** pm ET**

---

[**Join Zoom Meeting**](https://us06web.zoom.us/j/88139848852) | Meeting ID: 881 3984 8852 | one touch dial-in: \+16465588656,,88139848852\#   
[**Meeting Recording and Transcript**](https://fathom.video/share/WT6U2XeCkdSvzxRHzJCVQSUsyQ1HwsNt) | **[Link to this Document]()** | [Link to Town Halls Folder](https://drive.google.com/drive/folders/1UBD-b4l3wXfu4rNwwsLw6NiP5hoQY67z?usp=share...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/104999059

---

## CASE 48: Lee G

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 1 meeting(s)
- **2023-05-24:** ...The Education Fund  
	https://www.educationfund.org/what-we-do/programs/food-forests-for-schools/participating-schools.html  
16:16:02 From **Lee G** to Everyone:  
	Reacted to "For more info on ani..." with 👍  
16:16:18 From **Lee G** to Everyone:  
	Reacted to "51 schools in Dade C..." with 😍  
16:17:15 From **Lee G** to Everyone:  
	Reacted to...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/39937391, https://fathom.video/calls/22368500

---

## CASE 49: Leonard

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-09-17:** ...Totimeh, Folonrunsho Dayo, **Leonard** Iyamuremye, Milt Markewitz, Ir Marius, Abby Karparis, Indy Singh, Jan Dietrich; Louise Mitchell, Edib Korkut, Mayaya Mack, Poulomi Chakravarty; Edward Paul Munaaba, Betty Bitengo; Mara Huber

**Presentations:**

[Diana Doheny](https://www.linkedin.com/in/diana-doheny/), ERA Communications Committee ([member feedback survey](https://docs.google.com/forms/d/1b-bkn64cCnlKlVVjuqvR0I3-A7heOzR2HneQF79BlhE/edit))

[Eduard Müller](https://www...
- **2025-06-25:** ...Jon Schull, Poulomi Chakravarty, Charles Upton, Johan Myrberger, Jonathan Cloud, Louise Mitchell, Natalie Fleming, Ananda Fitzsimmons, **Leonard** Iyamuremye, Brian von Herzen, Ana Calderon, Daniel Langfitt, Edward Paul Munaaba, Betty Bitengo, Konrad Borowski, Daniel Langfitt

Updates and Introductions:

Ana Calderon: Panama Biofi presentation

[Konrad Borowski](https://www.linkedin.com/in/konradborowski/): Beekon flood-resistant beehives

[Dan Langfitt](https://www.linkedin.com...
- **2025-05-28:** ...This is more than theory—it’s an invitation to design and inhabit regenerative systems rooted in action, reciprocity, and care.

![][image2]![][image3]

Jon Schull, Edward Paul, Aude Peronne, Denise Pang, Alex Bai, Russ Speer, Charslse Upton, Twizeyimana Innocent, Katie Chess, Did Pershouse, Richelle Steyn, Kevin Maher, **Leonard** Iyamuremye, Edward Muller, Herb Simmens, Mick Lorkins, Grant Holton, Gayathri Ilango, Kimberly...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/394570977, https://fathom.video/calls/381363934, https://fathom.video/calls/355913725, https://fathom.video/calls/343485589, https://fathom.video/calls/414406098

---

## CASE 50: Leonard IYAMUREME

**Category:** unknown
**Fathom records:** 1

**Town Hall:** Found in 3 meeting(s)
- **2025-02-05:** ...org/donate)

**Participants:**   
Jon Schull, Philip Bogdonoff, Robert Patterson, Marie Arbelias (Evolutesix), Johan Myrberger, Jonathan Cloud & Victoria Zelin, Natalie Fleming, Paolo Nardi, Graham Boyd (Evolutesix), Michael Pilarski, Donna Nelham, **Leonard Iyamureme**, Andrea Manrique Yus (Spain), Rodger Savory, Dan Kittredge, James Arnott (Orbis Expeditions), Mark Haubner, Ian Redmond, Andrea Manrique, Ananda Fitzsimmons, Mohammed Alkhalid, Ansima Casinga “Rolande” (For the Love of...
- **2025-01-08:** ...Bogdonoff, Mike Lynn, Kyle Lawson, Michael Pilarski (Global Earth Repair Convergence), Zach Weiss (Water Stories), Samantha Power, Judith Schwartz, Simone Ticehurst, Russ Speer, James Conway, Bru Pearce, Grant Holton, **Leonard Iyamureme**, BasHam Zain, Edward Paul Munaaba, Edib Korkut, Phoebe Barnard (Global Restoration Collaborative, Stable Planet Alliance), Ellie Young, Rodger Savory, Natalie Fleming, Ananda Fitzsimmons, Jan-Philip Wassenaar, Jonathan Cloud & Victoria...
- **2024-12-18:** ...experience.arcgis.com/experience/40da4f30e90f4578b84cb9f4353308a6) | [**Donate\!**](http://EcoRestorationAlliance.org/donate)

**Participants:**   
Jon Schull, Mark Haubner, Bru Pearce, Ananda Fitsimmons, Joe James, Jme Conway, Mike Lynn, Renee Cho, Diana Doheny, **Leonard Iyamureme** (Rwanda), Fred Jennings, Russ Speer, Charles Upton, Mbilizi Kalombo (Nakivale), Jonathan Cloud & Victoria Zelin, Philip Bogdonoff, Colleen Dick, Dennis Garrity (based in the Philippines; GEA; also HPAC), Charles Upton...

**Gmail:** Not found

**Airtable:** No match found

**Fathom recording:** https://fathom.video/calls/319553577, https://fathom.video/calls/308230203, https://fathom.video/calls/285085815, https://fathom.video/calls/263417891, https://fathom.video/calls/253037687, https://fathom.video/calls/242890812, https://fathom.video/calls/233189775, https://fathom.video/calls/223525279, https://fathom.video/calls/214375292, https://fathom.video/calls/205793805, https://fathom.video/calls/201817513, https://fathom.video/calls/193558243, https://fathom.video/calls/324278211, https://fathom.video/calls/301421112, https://fathom.video/calls/267833235, https://fathom.video/calls/257059280, https://fathom.video/calls/209204233, https://fathom.video/calls/200959970, https://fathom.video/calls/181365987, https://fathom.video/calls/174035176, https://fathom.video/calls/226162234

---
