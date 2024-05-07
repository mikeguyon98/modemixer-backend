# ModeMixer Backend

The **ModeMixer Backend** provides a FastAPI-based RESTful API that serves as the backbone for the ModeMixer web application. It powers AI-driven fashion design pipelines by interacting with OpenAI models, MongoDB, and other components.


- [How To Run API](#run-instruct)
- [Tech Stack](#tech-stack)
- [Responsible AI Principles](#responsible-ai-principles)
- [License](#license)

## How To Run API
- get .env file
- run `uvicorn app.main:app --reload`

## Tech Stack
- **Framework:** FastAPI
- **Database:** MongoDB
- **AI Models:** Azure OpenAI Service (GPT, DALL-E)
- **Deployment:** Azure App Service

## Responsible AI Principles

In developing ModeMixer, we integrated Responsible AI principles to ensure fairness, transparency, and inclusivity:

Fairness:
- Diverse Data Sources: Incorporating a variety of fashion trends and styles to represent different cultures, genders, and body types.
- Bias Mitigation: Curated data to avoid overrepresentation of any specific demographic.

Transparency:
- User Control: Allowing users to modify designs and descriptions.

Privacy and Security:
- Data Protection: Securely storing user data and collections.
- Minimal User Data Collection: Collecting only necessary data to create designs and tech packs.

Inclusivity:
- Customizable Descriptions: Allowing users to customize collection descriptions.
- Accessible Tech Packs: Providing tech packs in accessible formats (PDF).

Reliability and Safety:
- Continuous Improvement: Regularly updating the knowledge base.

## License

ModeMixer is licensed under the [MIT License](https://opensource.org/licenses/MIT).

