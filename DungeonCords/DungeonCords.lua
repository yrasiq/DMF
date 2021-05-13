local math = getfenv(0).math

SLASH_HELLO_WORLD1 = '/helloworld';
Disenchant = 1

local EventFrame = CreateFrame("Frame") 
local HelloWorld1 = CreateFrame("Frame", nil, UIParent) 
local HelloWorld2 = CreateFrame("Frame", nil, UIParent)
local HelloWorld3 = CreateFrame("Frame", nil, UIParent)
local HelloWorld4 = CreateFrame("Frame", nil, UIParent)
local HelloWorld5 = CreateFrame("Frame", nil, UIParent)
local HelloWorld6 = CreateFrame("Frame", nil, UIParent)
local HelloWorld7 = CreateFrame("Frame", nil, UIParent)
local HelloWorld8 = CreateFrame("Frame", nil, UIParent)
local HelloWorld9 = CreateFrame("Frame", nil, UIParent)
local HelloWorld10 = CreateFrame("Frame", nil, UIParent)
local HelloWorld11 = CreateFrame("Frame", nil, UIParent)
local btn = CreateFrame("Button", nil, UIParent, "SecureActionButtonTemplate, UIPanelButtonTemplate")
function EventFrame:OnEvent(event, ...) 
	self[event](self, ...) 
end
EventFrame:SetScript("OnEvent", EventFrame.OnEvent)

EventFrame:RegisterEvent("PLAYER_LOGIN")
function EventFrame:PLAYER_LOGIN() 
	btn:SetPoint("BOTTOMLEFT", 50, 50)
	btn:SetSize(100, 40)
	btn:SetText("Распылить")
	btn:HookScript("OnMouseUp", function(self, button)
		Disenchant = 255
		local slotinbug = 0
		local numslot = 1
		local _, _, itemRarity, _, _, _, _, _, _, _, _, itemClassID, _, _, _, _, _
		local itemName, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _
		local itemName = nil
		local itemRarity = nil
		local itemClassID = nil
		btn:SetAttribute("type", nil)
		btn:SetAttribute("spell", nil)
		btn:SetAttribute("target-item", nil)
		for i=0,4 do
			slotinbug = GetContainerNumSlots(i)
			for i2=1,slotinbug do
				numslot = GetContainerItemLink(i, i2)
				if numslot ~= nil then _, _, itemRarity, _, _, _, _, _, _, _, _, itemClassID, _, _, _, _, _ = GetItemInfo(numslot)
					if (itemRarity == 2 or itemRarity == 3) and (itemClassID == 2 or itemClassID == 4) then
						itemName, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = GetItemInfo(numslot)
						btn:SetAttribute("type", "spell")
						btn:SetAttribute("spell", "Разрушение чар")
						btn:SetAttribute("target-item", itemName)
					end
				end
			end
		end
		if itemName == nil then
			Disenchant = 1
			print("Нечего распылять")
		end
	end)
	HelloWorld1:SetFrameStrata("BACKGROUND")
	HelloWorld1:SetWidth(10) 
	HelloWorld1:SetHeight(10) 
	HelloWorld1.texture = HelloWorld1:CreateTexture(nil,"BACKGROUND")
	HelloWorld1.texture:SetAllPoints(HelloWorld1)
	HelloWorld1:SetPoint("TOPLEFT",0,0)
	HelloWorld1:Show()

	HelloWorld2:SetFrameStrata("BACKGROUND")
	HelloWorld2:SetWidth(10) 
	HelloWorld2:SetHeight(10) 
	HelloWorld2.texture = HelloWorld2:CreateTexture(nil,"BACKGROUND")
	HelloWorld2.texture:SetAllPoints(HelloWorld2)
	HelloWorld2:SetPoint("TOPLEFT",10,0)
	HelloWorld2:Show()

	HelloWorld3:SetFrameStrata("BACKGROUND")
	HelloWorld3:SetWidth(10) 
	HelloWorld3:SetHeight(10) 
	HelloWorld3.texture = HelloWorld3:CreateTexture(nil,"BACKGROUND")
	HelloWorld3.texture:SetAllPoints(HelloWorld3)
	HelloWorld3:SetPoint("TOPLEFT",20,0)
	HelloWorld3:Show()

	HelloWorld4:SetFrameStrata("BACKGROUND")
	HelloWorld4:SetWidth(10) 
	HelloWorld4:SetHeight(10) 
	HelloWorld4.texture = HelloWorld4:CreateTexture(nil,"BACKGROUND")
	HelloWorld4.texture:SetAllPoints(HelloWorld4)
	HelloWorld4:SetPoint("TOPLEFT",30,0)
	HelloWorld4:Show()

	HelloWorld5:SetFrameStrata("BACKGROUND")
	HelloWorld5:SetWidth(10) 
	HelloWorld5:SetHeight(10) 
	HelloWorld5.texture = HelloWorld5:CreateTexture(nil,"BACKGROUND")
	HelloWorld5.texture:SetAllPoints(HelloWorld5)
	HelloWorld5:SetPoint("TOPLEFT",40,0)
	HelloWorld5:Show()

	HelloWorld6:SetFrameStrata("BACKGROUND")
	HelloWorld6:SetWidth(10) 
	HelloWorld6:SetHeight(10) 
	HelloWorld6.texture = HelloWorld6:CreateTexture(nil,"BACKGROUND")
	HelloWorld6.texture:SetAllPoints(HelloWorld6)
	HelloWorld6:SetPoint("TOPLEFT",50,0)
	HelloWorld6:Show()

	HelloWorld7:SetFrameStrata("BACKGROUND")
	HelloWorld7:SetWidth(10) 
	HelloWorld7:SetHeight(10) 
	HelloWorld7.texture = HelloWorld7:CreateTexture(nil,"BACKGROUND")
	HelloWorld7.texture:SetAllPoints(HelloWorld7)
	HelloWorld7:SetPoint("TOPLEFT",60,0)
	HelloWorld7:Show()

	HelloWorld8:SetFrameStrata("BACKGROUND")
	HelloWorld8:SetWidth(10) 
	HelloWorld8:SetHeight(10) 
	HelloWorld8.texture = HelloWorld8:CreateTexture(nil,"BACKGROUND")
	HelloWorld8.texture:SetAllPoints(HelloWorld8)
	HelloWorld8:SetPoint("TOPLEFT",70,0)
	HelloWorld8:Show()

	HelloWorld9:SetFrameStrata("BACKGROUND")
	HelloWorld9:SetWidth(10) 
	HelloWorld9:SetHeight(10) 
	HelloWorld9.texture = HelloWorld9:CreateTexture(nil,"BACKGROUND")
	HelloWorld9.texture:SetAllPoints(HelloWorld9)
	HelloWorld9:SetPoint("TOPLEFT",80,0)
	HelloWorld9:Show()

	HelloWorld10:SetFrameStrata("BACKGROUND")
	HelloWorld10:SetWidth(10) 
	HelloWorld10:SetHeight(10) 
	HelloWorld10.texture = HelloWorld10:CreateTexture(nil,"BACKGROUND")
	HelloWorld10.texture:SetAllPoints(HelloWorld10)
	HelloWorld10:SetPoint("TOPLEFT",90,0)
	HelloWorld10:Show()

	HelloWorld11:SetFrameStrata("BACKGROUND")
	HelloWorld11:SetWidth(10) 
	HelloWorld11:SetHeight(10) 
	HelloWorld11.texture = HelloWorld11:CreateTexture(nil,"BACKGROUND")
	HelloWorld11.texture:SetAllPoints(HelloWorld11)
	HelloWorld11:SetPoint("TOPLEFT",100,0)
	HelloWorld11:Show()
end 
function EventFrame:OnUpdate() 
	local target = UnitExists("target")
	local status = UnitIsDead("target")
	local range1 = CheckInteractDistance("target", 3)
	local range24 = IsSpellInRange("Похищение жизни", "target")
	local range30 = IsSpellInRange("Стрела тьмы", "target")
	local range36 = IsSpellInRange("Порча", "target")
	local dist = 0
	local immolate = 1
	local corrapt = 1
	local demoskin = 1
	local soulstonebuff = 1
	local spell = CastingInfo()
	local pet = PetHasActionBar()
	local combat = InCombatLockdown()
	local health = (UnitHealth("player")/UnitHealthMax("player"))*100
	local healthtarget = (UnitHealth("target")/UnitHealthMax("target"))*100
	local healthpet = 255
	local power = (UnitPower("player", 0)/UnitPowerMax("player", 0))*100
	local curse = 1
	local sifon = 1
	local lifedrain = 1
	local souldrain = 1
	local demon_s = 1
	local eat = 1
	local drink = 1
	local healstone = GetItemCount("Крупный камень здоровья")
	local soulstone = GetItemCount("Крупный камень души")
	local shard = GetItemCount("Осколок души") + 1
	local healstonecd = GetActionCooldown(57) + 1
	local soulstonecd = GetActionCooldown(59) + 1
	local coilcd = GetActionCooldown(12) + 1
	local nightfall = 1
	local stealth = 1
	local playerslow = 1
	local dead = UnitIsDeadOrGhost('player')
	local durancyitem = 100
	for i=1,18 do
		local current, maximum = GetInventoryItemDurability(i)
		if current ~= nil and maximum ~= nil then
			if math.floor((current/maximum) * 100) < durancyitem then durancyitem = math.floor((current/maximum) * 100) end
		end
	end
	for i=1,40 do
		local name, _, _, _, etime, _, source = UnitDebuff("target", i)
		if name == "Жертвенный огонь" and source == "player" then immolate = 255 end
		if name == "Порча" and source == "player" then corrapt = 255 end
		if name == "Проклятие агонии" and source == "player" then curse = 255 end
		if name == "Вытягивание жизни" and source == "player" then sifon = 255 end
		if name == "Похищение жизни" and source == "player" then lifedrain = 255 end
		if name == "Похищение души" and source == "player" then souldrain = 255 end
	end
	for i=1,40 do
		local name, _, _, _, etime, _, source = UnitBuff("player", i)
		if name == "Демонический доспех" and source == "player" then demoskin = 255 end
		if name == "Воскрешение камнем души" and source == "player" then soulstonebuff = 255 end
		if name == "Теневой транс" and source == "player" then nightfall = 255 end
		if name == "Выносливость скверны" and source == "player" then demon_s = 255 end
		if name == "Пища" and source == "player" then eat = 255 end
		if name == "Питье" and source == "player" then drink = 255 end
		if (name == "Невидимость" and source == "player") or (name == "Малая невидимость" and source == "player") then stealth = 255 end
	end
	for i=1,40 do
		local name, _, _, _, etime, _, source = UnitDebuff("player", i)
		if name == "Замедляющий яд" then playerslow = 255 end
	end
	if target == false then target = 1 else target = 255 end
	if status == false then status = 1 else status = 255 end
	if range1 == true then dist = 0.1 end
	if range1 == false and range24 == 1 then dist = 0.24 end
	if range24 == 0 and range30 == 1 then dist = 0.30 end
	if range30 == 0 and range36 == 1 then dist = 0.36 end
	if range36 == 0 then dist = 1 end
	if pet == false then pet = 0 else pet = 1 end
	if combat == false then combat = 1 else combat = 255 end
	if spell == nil then spell = 1 else spell = 255 end
	if healstone == 0 then healstone = 1 else healstone = 255 end
	if soulstone == 0 then soulstone = 1 else soulstone = 255 end
	if pet == 1 then healthpet = (UnitHealth("pet")/UnitHealthMax("pet"))*100 end
	if dead == true then dead = 1 else dead = 255 end

	HelloWorld1.texture:SetColorTexture(playerslow/255, eat/255, drink/255)
	HelloWorld2.texture:SetColorTexture(stealth/255, demon_s/255, health/255)
	HelloWorld3.texture:SetColorTexture(target/255, status/255, dist)
	HelloWorld4.texture:SetColorTexture(immolate/255, corrapt/255, power/255)
	HelloWorld5.texture:SetColorTexture(demoskin/255, pet/255, combat/255)
	HelloWorld6.texture:SetColorTexture(curse/255, spell/255, healthtarget/255)
	HelloWorld7.texture:SetColorTexture(healstonecd/255, soulstonecd/255, soulstonebuff/255)
	HelloWorld8.texture:SetColorTexture(healstone/255, soulstone/255, shard/255)
	HelloWorld9.texture:SetColorTexture(healthpet/255, nightfall/255, sifon/255)
	HelloWorld10.texture:SetColorTexture(coilcd/255, lifedrain/255, souldrain/255)
	HelloWorld11.texture:SetColorTexture(dead/255, Disenchant/255, durancyitem/255)
end

EventFrame:RegisterEvent("PLAYER_TARGET_CHANGED")
function EventFrame:PLAYER_TARGET_CHANGED()
	local target = UnitExists("target")
	local status = UnitIsDead("target")
	if target == false then target = 1 else target = 255 end
	if status == false then status = 1 else status = 255 end
end

EventFrame:SetScript("OnUpdate", EventFrame.OnUpdate)

function SlashCmdList.HELLO_WORLD(msg, editbox)
	local durancyitem = 100
	for i=1,18 do
		local current, maximum = GetInventoryItemDurability(i)
		if current ~= nil and maximum ~= nil then
			if math.floor((current/maximum) * 100) < durancyitem then durancyitem = math.floor((current/maximum) * 100) end
		end
	end
	print(durancyitem)
end