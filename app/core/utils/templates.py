from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

def render_template(
    request: Request, template_name: str, context: dict
):
    """
    Renders either a full page (base.html) or just the partial content based on HTMX request.
    
    Args:
        request (Request): The FastAPI request object.
        template_name (str): The template to render.
        context (dict): Context data for the template.
    
    Returns:
        TemplateResponse: The correct template based on whether it's an HTMX request.
    """
    if request.headers.get("HX-Request"):
        # Return the partial template without base.html
        return templates.TemplateResponse(f"partials/{template_name}", context)
    else:
        # Return the full template extending base.html
        return templates.TemplateResponse(f"pages/{template_name}", context)
