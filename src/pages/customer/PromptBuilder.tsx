
import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Copy, RefreshCw, ArrowDown } from "lucide-react";
import { toast } from "sonner";

const PromptBuilder: React.FC = () => {
  const [template, setTemplate] = useState<string>("uppdrag");
  const [customerText, setCustomerText] = useState<string>("");
  const [category, setCategory] = useState<string>("resa");
  const [department, setDepartment] = useState<string>("trafikledningen");
  const [completionType, setCompletionType] = useState<string>("information");
  const [language, setLanguage] = useState<string>("svenska");
  const [closingText, setClosingText] = useState<string>("trevlig-resa");
  const [previewText, setPreviewText] = useState<string>("");
  const [route, setRoute] = useState<string>("");
  const [date, setDate] = useState<string>("2023-03-26");
  const [time, setTime] = useState<string>("15:30");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [hasPII, setHasPII] = useState<boolean>(false);

  // Handle sensitive information detection (PII)
  useEffect(() => {
    // Simple regex to detect potential Swedish personal identity numbers (personnummer)
    const piiRegex = /\b\d{6}[-\s]?\d{4}\b/g;
    const hasPIIInfo = piiRegex.test(customerText);
    setHasPII(hasPIIInfo);
  }, [customerText]);

  // Update preview in real-time
  useEffect(() => {
    updatePreview();
  }, [customerText, category, department, completionType, language, closingText, route, date, time]);

  const updatePreview = () => {
    // This would typically fetch from your backend
    // For demo purposes, we'll generate a static preview
    let destination = "";

    if (route.includes("Malmö")) {
      destination = "Malmö";
    } else if (route.includes("Stockholm")) {
      destination = "Stockholm";
    } else {
      destination = route.split("-")[1]?.trim() || "destination";
    }

    let preview = `Ämne: Angående din tågresa till ${destination}\n\nHej!\n\n`;

    // Add the customer's text info without PII
    let sanitizedText = customerText;
    if (hasPII) {
      sanitizedText = customerText.replace(/\b\d{6}[-\s]?\d{4}\b/g, "XXXXXX-XXXX");
    }
    
    // Format based on category and completion type
    if (category === "resa") {
      preview += `Tack för ditt meddelande angående din tågresa till ${destination} den ${date}.\n\n`;
      
      if (completionType === "information") {
        preview += `Vi kan bekräfta att din bokning med koden ABC123 finns i vårt system för avgången klockan ${time} från Stockholm C.\n\n`;
        preview += `För att kunna hjälpa dig vidare behöver vi följande information:\n\n`;
        preview += `- Vad undrar du specifikt angående din resa?\n`;
        preview += `- Har du några särskilda behov inför resan?\n\n`;
      }
    } else if (category === "ersattning") {
      preview += `Tack för ditt meddelande angående ersättning.\n\n`;
      preview += `Vi behöver mer information för att hantera ditt ärende. Vänligen skicka in följande:\n\n`;
      preview += `- Ditt bokningsnummer\n`;
      preview += `- Datum och tid för resan\n`;
      preview += `- Beskrivning av vad som hände\n\n`;
    } else if (category === "klagomal") {
      preview += `Tack för ditt meddelande. Vi beklagar att du har upplevt problem med vår tjänst.\n\n`;
      preview += `Vi tar ditt klagomål på största allvar och kommer att utreda detta noggrant.\n\n`;
    }

    preview += `Din fråga kommer att hanteras av ${department} som återkommer så snart som möjligt med mer information.\n\n`;
    
    // Add closing
    if (closingText === "trevlig-resa") {
      preview += `Med vänliga hälsningar,\nKundtjänst\nTrevlig resa!`;
    } else {
      preview += `Med vänliga hälsningar,\nKundtjänst`;
    }

    setPreviewText(preview);
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(previewText);
    toast.success("Kopierat till urklipp!");
  };

  const handleReset = () => {
    setCustomerText("");
    setCategory("resa");
    setDepartment("trafikledningen");
    setCompletionType("information");
    setLanguage("svenska");
    setClosingText("trevlig-resa");
    setRoute("");
    setDate("2023-03-26");
    setTime("15:30");
    setIsLoading(true);
    
    setTimeout(() => {
      setIsLoading(false);
      toast.success("Formuläret har återställts");
    }, 500);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-7xl mx-auto">
      {/* Customer Query Section */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-promptBlue px-4 py-2 bg-white rounded-t-lg border-b">Kundförfrågan</h2>
        <div className="prompt-section">
          <div className="mb-4">
            <Label htmlFor="template">Välj mall</Label>
            <Select 
              value={template} 
              onValueChange={setTemplate}
            >
              <SelectTrigger>
                <SelectValue placeholder="Välj mall" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="uppdrag">Uppdrag</SelectItem>
                <SelectItem value="support">Support</SelectItem>
                <SelectItem value="information">Information</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="mb-4">
            <Label htmlFor="customer-text" className="mb-2 block">Kundtext</Label>
            <Textarea 
              id="customer-text"
              placeholder="Klistra in kundens text här..."
              className="min-h-32"
              value={customerText}
              onChange={(e) => setCustomerText(e.target.value)}
            />
            {hasPII && (
              <p className="text-xs text-promptRed mt-1 flex items-center gap-1">
                <span className="bg-promptRed/20 text-promptRed px-1.5 py-0.5 rounded text-xs font-medium">PII DETECTED</span> 
                Personnummer har upptäckts och maskerats i förhandsgranskningen
              </p>
            )}
          </div>
          
          <div className="flex justify-between">
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleReset}
              className="text-xs"
            >
              <RefreshCw className="h-3 w-3 mr-1" /> 
              Återställ formulär
            </Button>
          </div>
        </div>
      </div>
      
      {/* Form Options Section */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-promptBlue px-4 py-2 bg-white rounded-t-lg border-b">Formuläralternativ</h2>
        <div className="prompt-section">
          <div className="mb-4">
            <Label className="mb-2 block">Kategori</Label>
            <div className="grid grid-cols-3 gap-2">
              <button 
                className={`category-pill ${category === 'resa' ? 'active' : 'inactive'}`}
                onClick={() => setCategory('resa')}
              >
                <span className="h-2 w-2 rounded-full bg-current" /> Resa
              </button>
              <button 
                className={`category-pill ${category === 'ersattning' ? 'active' : 'inactive'}`}
                onClick={() => setCategory('ersattning')}
              >
                <span className="h-2 w-2 rounded-full bg-current" /> Ersättning
              </button>
              <button 
                className={`category-pill ${category === 'klagomal' ? 'active' : 'inactive'}`}
                onClick={() => setCategory('klagomal')}
              >
                <span className="h-2 w-2 rounded-full bg-current" /> Klagomål
              </button>
            </div>
          </div>
          
          <div className="mb-4">
            <Label htmlFor="department">Avdelning</Label>
            <Select 
              value={department}
              onValueChange={setDepartment}
            >
              <SelectTrigger id="department">
                <SelectValue placeholder="Välj avdelning" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="trafikledningen">Trafikledningen</SelectItem>
                <SelectItem value="kundservice">Kundservice</SelectItem>
                <SelectItem value="ekonomi">Ekonomi</SelectItem>
                <SelectItem value="kvalitet">Kvalitet</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="mb-4">
            <Label htmlFor="completion-type">Kompletteringstyp</Label>
            <Select
              value={completionType}
              onValueChange={setCompletionType}
            >
              <SelectTrigger id="completion-type">
                <SelectValue placeholder="Välj kompletteringstyp" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="information">Information</SelectItem>
                <SelectItem value="tidtabell">Tidtabell</SelectItem>
                <SelectItem value="ersattning">Ersättning</SelectItem>
                <SelectItem value="klagomal">Klagomål</SelectItem>
                <SelectItem value="forsening">Försening</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          {category === 'resa' && (
            <Card className="mb-4 border border-border shadow-none">
              <CardContent className="p-4 space-y-4">
                <h4 className="font-medium text-sm">Resedetaljer</h4>
                
                <div>
                  <Label htmlFor="route">Linje/Sträcka:</Label>
                  <Input 
                    id="route"
                    placeholder="T.ex. Stockholm C - Malmö C"
                    value={route}
                    onChange={(e) => setRoute(e.target.value)}
                  />
                </div>
                
                <div>
                  <Label htmlFor="date">Datum:</Label>
                  <Input 
                    id="date"
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                  />
                </div>
                
                <div>
                  <Label htmlFor="time">Tid:</Label>
                  <Input 
                    id="time"
                    type="time"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                  />
                </div>
              </CardContent>
            </Card>
          )}
          
          <div className="mb-4">
            <Label className="mb-2 block">Språk</Label>
            <div className="grid grid-cols-2 gap-2">
              <button 
                className={`category-pill ${language === 'svenska' ? 'active' : 'inactive'}`}
                onClick={() => setLanguage('svenska')}
              >
                <span className="h-2 w-2 rounded-full bg-current" /> Svenska
              </button>
              <button 
                className={`category-pill ${language === 'engelska' ? 'active' : 'inactive'}`}
                onClick={() => setLanguage('engelska')}
              >
                <span className="h-2 w-2 rounded-full bg-current" /> Engelska
              </button>
            </div>
          </div>
          
          <div className="mb-4">
            <Label htmlFor="closing-text">Avslutningstext</Label>
            <Select
              value={closingText}
              onValueChange={setClosingText}
            >
              <SelectTrigger id="closing-text">
                <SelectValue placeholder="Välj avslutningstext" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="trevlig-resa">Trevlig resa!</SelectItem>
                <SelectItem value="standard">Standard</SelectItem>
                <SelectItem value="tacksam">Tacksam för återkoppling</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
      
      {/* Preview Section */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-promptBlue px-4 py-2 bg-white rounded-t-lg border-b">Förhandsgranskning</h2>
        <div className="prompt-section">
          <div className="whitespace-pre-wrap bg-white border border-gray-200 rounded-lg p-4 min-h-[400px] text-left relative">
            {isLoading ? (
              <div className="flex justify-center items-center h-full">
                <div className="animate-spin h-6 w-6 border-2 border-promptBlue border-t-transparent rounded-full"></div>
              </div>
            ) : (
              <>
                {previewText}
              </>
            )}
          </div>
          
          <div className="mt-4 space-y-2">
            <Button 
              className="w-full bg-promptBlue hover:bg-promptBlue-800"
              onClick={handleCopyToClipboard}
            >
              <Copy className="h-4 w-4 mr-2" /> Kopiera till Urklipp
            </Button>
            
            <Button 
              variant="outline" 
              className="w-full" 
              onClick={handleReset}
            >
              <ArrowDown className="h-4 w-4 mr-2" /> Återställ Formulär
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PromptBuilder;
