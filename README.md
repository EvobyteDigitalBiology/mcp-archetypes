# 🏗️ MCP Archetypes

**A comprehensive collection of architectural patterns for building Model Context Protocol (MCP) clients and servers**

Welcome to MCP Archetypes! This repository showcases various architectural patterns, frameworks, transport mechanisms, and authentication strategies for developing robust MCP applications. Whether you're building weather services, data analysis tools, or complex AI-powered applications, these archetypes provide battle-tested foundations to accelerate your development.

Get in touch to submit ideas, comments or new patterns.

## 🚀 What's Inside

MCP Archetypes demonstrates implementations of MCP clients and servers using different frameworks, transports and authorization methods for different aspect of the MCP Specification.
The server implementations use simple, repeated functionalities like calls to the weather.gov API, as presented in the excellent [Quickstart](https://modelcontextprotocol.io/quickstart/server) guide by the MCP Authors.

The focus of this collection is how to architect MCP servers and clients for different tech stacks, auth requirements and interfaces.


### 📊 Architecture Matrix

This table is an overview of example implementations for server and client scripts presented in this repository.

| **Script** | Type | MCP Feature | Transport | Auth | Description |
|-----------|-----------|-----------|-----------|----------------|-------|
| [io_api_server.py](#ioapiserver) | Server | Tools | STDIO | None  | MCP Tools Server Weather API |
| [io_api_sampling_server.py](#ioasamplingserver) | Server | Tools, Client Sampling | STDIO | None  | Space News API with LLM-powered translation |
| [io_resource_server.py](#ioresourceserver) | Server | Resources | STDIO | None  | Static and dynamic Resources |
| [io_prompt_server.py](#iopromptserver) | Server | Prompts | STDIO | None  | Blog Generation Prompt Templates with Code Analysis |
| [io_tools_client_bedrock.py](#iotoolsclientbedrock)  | Client | Tools | STDIO | None | AWS Bedrock integration (Converse API) for MCP Tools |
| [io_prompt_client_bedrock.py](#iopromptclientbedrock) | Client | Prompts | STDIO | None | AWS Bedrock using MCP Prompts |
| [io_resources_client_bedrock.py](#ioresourcesclientbedrock)  | Client | Resources | STDIO | None | AWS Bedrock integration (Converse API) for MCP Resources |


## 🔧 Architecture Patterns

### 1. **Server-Side Patterns**

#### FastMCP Pattern
- **Use Case**: High-performance servers with minimal boilerplate
- **Benefits**: Built-in transport handling, automatic tool registration, provisioning of resources
- **Best For**: Production services, API integrations

#### Transport Flexibility
- **STDIO**: Perfect for local development and direct client connections
- **HTTP**: Ideal for web-based clients and microservice architectures

### 2. **Client-Side Patterns**

#### AWS Bedrock Integration
- **Use Case**: Integration of FastMCP with Bedrock Models
- **Components**: Different APIs, such as Converse API or Bedrock Agents

#### FastMCP Pattern
-  **Use Case**: High-performance clients with minimal boilerplate
-  Rapid server connection and handling 

#### Authentication Strategies
- **AWS Bedrock**: Enterprise-grade AI with managed authentication
- **Environment Variables**: Secure credential management
- **Token-based**: Scalable authentication for distributed systems

### 3. **Transport Patterns**

#### STDIO Transport
```python
# Server setup
mcp.run(transport='stdio')

# Client connection
server_params = StdioServerParameters(
    command='python3',
    args=[server_script_path, 'local']
)
```

#### HTTP Transport
```python
# Server setup
mcp.run(transport='http')

# Client connection (future archetype)
# HTTP client implementation coming soon
```

## 🌟 Module Details

### `io_api_server.py`: Weather Data Tool MCP Server <a id="ioapiserver"></a>
A production-ready MCP server that provides comprehensive weather information using the National Weather Service API.

**🎯Features:**
- **FastMCP Framework**: Lightning-fast server implementation
- **Real-time Weather Data**: Current conditions and forecasts
- **Alert System**: Weather warnings and advisories
- **Dual Transport**: Supports both STDIO and HTTP transports
- **Error Handling**: Robust error management for external API calls

**🔧Tools Provided:**
- `get_alerts(state)` - Retrieve active weather alerts for any US state
- `get_forecast(latitude, longitude)` - Get detailed weather forecasts for specific coordinates

**Transport**
- Local I/O Transport

**🛡️Required Auth & Credentials**
- None

<hr>

### `io_api_sampling_server.py`: Space News Server with Translation by LLM Sampling <a id="ioasamplingserver"></a>
An advanced MCP server that provides current space news with intelligent multilingual translation capabilities using LLM sampling, provisioned by the MCP client.

**🎯Features:**
- **FastMCP Framework**: High-performance server implementation with modern async architecture
- **Real-time Space News**: Fetches today's latest space news from SpaceflightNews API
- **LLM Translation**: Automatic translation to any language using LLM sampling via MCP Context

**🔧Tools Provided:**
- `get_todays_spacenews(language='EN')` - Retrieve today's space news with optional language translation
  - **Parameters**: 
    - `language` (str): ISO639 language code (default: 'EN')
  - **Returns**: JSON list with 'title' and 'summary' keys for each news article
  - **Features**: Automatic LLM-powered translation for non-English languages

**🛠️Technical Implementation:**
- **Data Source**: SpaceflightNews API v4 (https://api.spaceflightnewsapi.net/)
- **Translation Engine**: Context sampling with structured prompts and examples
- **Output Format**: Standardized JSON structure for easy client consumption

**📡API Details:**
- **Endpoint**: `/v4/articles/?published_at_gte={date.isoformat()}`
- **Response Processing**: Extracts title and summary from news articles

**Transport**
- Local I/O Transport (STDIO)

**🛡️Required Auth & Credentials**
- None (SpaceflightNews API is public)
- LLM Context access required for translation features

<hr>

### `io_resource_server.py`: Standard MCP Resource Server <a id="ioresourceserver"></a>
A comprehensive MCP server that demonstrates both static and dynamic resource provisioning using the FastMCP framework.

**🎯Features:**
- **FastMCP Framework**: High-performance resource server implementation
- **Static Resources**: File-based resources like documentation and configuration files
- **Dynamic Resources**: Template-based resources with parameterized URIs
- **Data Processing**: CSV file processing and JSON conversion capabilities
- **Sales Data Management**: Monthly sales data access and analysis

**📊Resources Provided:**
- `README` - Static markdown documentation resource
- `get_sales(year, month)` - Dynamic resource template for accessing monthly sales data

**🔧Resource Types:**
- **Static Resource**: README file served as a file resource with documentation metadata
- **Resource Template**: Parameterized URI pattern `resource://sales/{year}/{month}` for dynamic sales data access

**📁Example data:**
- CSV files organized by month and year (e.g., `january_2024.csv`)
- Automatic pandas DataFrame to JSON conversion
- Error handling for missing data files

**Transport**
- Local I/O Transport (STDIO)

**🛡️Required Auth & Credentials**
- None

<hr>

### `io_tools_client_bedrock.py`: Basic Bedrock AI Client with Tools Actions <a id="iotoolsclientbedrock"></a>
An intelligent MCP client that leverages AWS Bedrock's powerful language models to provide natural language interfaces to MCP tools.

**🎯Features:**
- **Example Function** Natural language query for weather forcast  
- **AWS Bedrock Integration**: Access to various models from AWS and external providers (e.g. Anthropic)
- **Dynamic Tool Calling**: Automatically invokes appropriate MCP tools

**🧠 Client:**
- AWS Bedrock Runtime
- Bedrock Converse API (AWS [Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html))
- Tool assess from AWS Converse API (AWS [Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-inference-call.html))

**Transport**
- Local I/O Transport

**🛡️Required Auth & Credentials**
- Boto3 Client Config
    - Region
- Environment variables
    - AWS_BEARER_TOKEN_BEDROCK
    
    OR
    
    - Configured IAM Role for Service running the client

    OR
    
    - Configured AWS CLI

    OR
    
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY

<hr>

### `io_resources_client_bedrock.py`: Bedrock AI Client "Sales Analysis" accessing MCP resources <a id="ioresourcesclientbedrock"></a>
An intelligent MCP client that connects to resource servers and leverages AWS Bedrock AI models to analyze and interpret resource data related to sales statistics.

**🎯Features:**
- **Resource Discovery**: Automatic listing and discovery of available resources and resource templates
- **AWS Bedrock Integration**: Utilizes Amazon models for natural language processing
- **Sales Data Analysis**: Example client for analyzing monthly sales data
- **Dynamic Resource Access**: Template-based resource retrieval with parameter substitution for reduced token usage
- **AI-Powered Insights**: Natural language querying of structured data

**🧠 AI Capabilities:**
- **Natural Language Queries**: Ask questions about sales data in plain English
- **Data Context Integration**: Combines resource documentation with data for enhanced analysis
- **Intelligent Responses**: Contextual analysis based on sales data and user queries

**🔧Resource Operations:**
- `list_resources()` - Discover available static resources
- `list_resource_templates()` - Find dynamic resource templates
- `read_resource(uri)` - Fetch resource content
- Template URI resolution with parameter substitution

**📊Data Processing:**
- CSV data retrieval and processing
- Integration with Bedrock Converse API
- System prompt construction with resource context
- Error handling for missing or invalid data

**Transport**
- Local I/O Transport (STDIO)

**🛡️Required Auth & Credentials**
- Boto3 Client Config
    - Region (us-east-1)
- Environment variables
    - AWS_BEARER_TOKEN_BEDROCK
    
    OR
    
    - Configured IAM Role for Service running the client

    OR
    
    - Configured AWS CLI

    OR
    
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY


### `io_prompt_server.py`: Blog Generation Prompt Templates with Code Analysis <a id="iopromptserver"></a>
A specialized MCP server that provides sophisticated prompt templates for automated blog post generation, featuring code analysis and content creation workflows tailored for technical documentation and data science audiences.

**🎯Features:**
- **FastMCP Framework**: High-performance prompt server implementation with tag-based organization
- **Multi-Stage Blog Generation**: Complete workflow from code analysis to final blog post compilation
- **Code Analysis**: Intelligent extraction of technology keywords from source code
- **Content Templates**: Structured prompts for intro, main content, and aggregation sections
- **Professional Tone**: Targeted at data science and development audiences

**🔧Prompts Provided:**

**Basic Interaction:**
- `greet_me(language='EN')` - Generate multilingual greetings using ISO 639 language codes

**Code Analysis Pipeline:**
- `get_keywords_from_code(code)` - Extract 5 relevant technology keywords from code samples
  - **Input**: Source code string
  - **Output**: JSON format with key "keywords" containing framework and protocol names
  - **Focus**: Excludes basic programming language elements, targets frameworks and libraries

**Content Generation:**
- `create_intro_from_code(keywords)` - Generate blog post introduction sections
  - **Input**: List of technology keywords
  - **Output**: 5-7 sentence professional introduction for data science audience
  
- `create_main_section_from_code(keywords, code)` - Create detailed main content
  - **Input**: Keywords list and source code
  - **Process**: Extracts 5 code sections, provides descriptions, aggregates into main content
  - **Output**: Technical blog post main section with code examples and explanations

**Content Assembly:**
- `aggregate_blog_sections(intro, main, outlook)` - Compile and polish complete blog posts
  - **Input**: Separate intro, main, and outlook sections
  - **Process**: Combines sections and polishes language for professional tone
  - **Output**: Complete, publication-ready blog post

**🛠️Technical Implementation:**
- **Prompt Structure**: Template-based approach with role definitions and clear task specifications
- **Output Format**: Structured JSON and markdown formats for different content types
- **Content Focus**: Specialized for technical and data science content creation
- **Tag System**: Organized with 'prompt' tags for easy categorization

**📝Content Workflow:**
1. **Code Input** → Keyword extraction via `get_keywords_from_code()`
2. **Keywords** → Introduction generation via `create_intro_from_code()`
3. **Keywords + Code** → Main content via `create_main_section_from_code()`
4. **All Sections** → Final assembly via `aggregate_blog_sections()`

**Transport**
- Local I/O Transport (STDIO)

**🛡️Required Auth & Credentials**
- None

**🎯Use Cases:**
- Automated technical documentation generation
- Blog post creation from code repositories
- Developer content workflows
- Data science project documentation

<hr>

### `io_prompt_client_bedrock.py`: Bedrock AI Client for Automated Blog Generation <a id="iopromptclientbedrock"></a>
An intelligent MCP client that leverages AWS Bedrock AI models to orchestrate automated blog post generation from source code using the prompt server's structured workflow.

**🎯Features:**
- **FastMCP Client Integration**: Seamless connection to MCP prompt servers using FastMCP framework
- **AWS Bedrock AI**: Utilizes DeepSeek R1 model for high-quality content generation
- **Automated Blog Workflow**: Complete end-to-end blog creation from source code input
- **Multi-Stage Processing**: Orchestrates keyword extraction, intro/main content generation, and final assembly
- **Professional Content**: Produces publication-ready blog posts for technical audiences

**🧠 AI-Powered Pipeline:**

**1. Code Analysis Phase:**
- `run_keyword_prompt(code)` - Extracts technology keywords from source code
- **Process**: Sends code to prompt server, processes JSON response with error handling
- **Output**: Clean list of relevant technology keywords

**2. Content Generation Phase:**
- `run_intro_prompt(keywords)` - Creates engaging introductions from keywords
- `run_main_prompt(keywords, code)` - Generates detailed main content with code analysis
- **Process**: Uses structured prompts via Bedrock Converse API
- **Focus**: Technical writing for data science and development audiences

**3. Assembly Phase:**
- `run_aggregate_prompt(intro, main, outlook)` - Compiles and polishes final blog post
- **Process**: Combines all sections and applies professional tone refinement
- **Output**: Complete, publication-ready blog post

**🔧Client Operations:**
- **Prompt Discovery**: `list_prompts()` - Discovers available prompts from connected server
- **Health Check**: `ping()` - Verifies server connectivity and responsiveness
- **File Processing**: Accepts code file paths and handles file reading automatically
- **Error Handling**: Robust JSON parsing with fallback error messages

**🛠️Technical Implementation:**
- **Model**: DeepSeek R1 (us.deepseek.r1-v1:0) via AWS Bedrock
- **Transport**: STDIO connection to MCP prompt server
- **Configuration**: AWS region-specific setup (us-east-1)
- **Environment**: Supports .env file for credential management

**📝Complete Workflow Example:**
```bash
python io_prompt_client_bedrock.py server_script.py source_code.py
```

**Process Flow:**
1. **Input**: Source code file → **Analysis**: Extract keywords
2. **Generation**: Create intro and main sections using AI
3. **Assembly**: Combine with outlook and polish for publication
4. **Output**: Complete blog post ready for publication

**🎯Specialized Features:**
- **JSON Response Parsing**: Handles code block removal and JSON cleaning
- **Hardcoded Keywords**: Uses ['MCP', 'FastMCP', 'Prompts'] for consistent branding
- **Outlook Integration**: Includes promotional content directing to www.evo-byte.com
- **Multi-Model Support**: Configurable for different Bedrock models

**Transport**
- Local I/O Transport (STDIO)

**🛡️Required Auth & Credentials**
- **AWS Bedrock Access**: 
  - Boto3 Client Config (Region: us-east-1)
  - DeepSeek R1 model access permissions
- **Environment Variables**:
  - AWS_BEARER_TOKEN_BEDROCK (OR configured IAM role/CLI/access keys)
- **Dependencies**: 
  - `python-dotenv` for environment management
  - `fastmcp` for MCP client functionality

**🎯Use Cases:**
- Automated developer documentation from codebases
- Technical blog generation for marketing teams  
- Developer relations content creation
- Code repository documentation automation
- Educational content generation from examples
    

## 🤝 Contributing

We welcome contributions! Here's how you can help expand MCP Archetypes:

1. **New Archetypes**: Add implementations for different frameworks
2. **Transport Patterns**: WebSockets, gRPC, message queues
3. **Authentication Methods**: OAuth, JWT, API keys
4. **Documentation**: Examples, tutorials, best practices

### Adding a New Archetype
1. Choose your framework/transport combination
2. Implement following the existing patterns
3. Add comprehensive documentation
4. Update the architecture matrix
5. Submit a pull request

## 📚 Resources

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [AWS Bedrock Developer Guide](https://docs.aws.amazon.com/bedrock/)
- [National Weather Service API](https://weather-gov.github.io/api/)
- [Spaceflight News API](https://spaceflightnewsapi.net/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎯 Ready to build your next MCP application?** Start with these archetypes and customize them for your specific needs. The patterns demonstrated here scale from simple prototypes to production-ready systems.
